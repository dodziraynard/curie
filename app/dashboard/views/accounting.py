import time
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from lms.utils.constants import InvoiceStatus

from dashboard.models import Klass, Student
from dashboard.tasks import update_students_account
from graphql_api.models.accounting import Invoice, InvoiceItem, Transaction
from lms.utils.constants import TransactionDirection, TransactionStatusMessages
from lms.utils.functions import make_model_key_value
from pdf_processor.tasks import generate_bulk_pdf_bill_sheet
from setup.models import SchoolSession
from django.utils import timezone


class AccountingIndexView(PermissionRequiredMixin, View):
    template_name = "dashboard/accounting/index.html"
    permission_required = [
        "setup.view_dashboard",
        "setup.manage_accounting",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        return render(request, self.template_name)


class InvoicesView(PermissionRequiredMixin, View):
    template_name = "dashboard/accounting/invoices.html"
    permission_required = [
        "setup.view_dashboard",
        "setup.manage_accounting",
        "setup.manage_accounting",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        query = request.GET.get("query")
        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")
        invoices = Invoice.objects.filter(deleted=False)
        if query:
            invoices = invoices.filter(name__icontains=query)
        if from_date:
            invoices = invoices.filter(created_at__gte=from_date)
        if to_date:
            invoices = invoices.filter(created_at__lte=to_date)
        invoices = invoices.order_by("-created_at")
        context = {
            "invoices": invoices[:300],
            "sessions": SchoolSession.objects.filter(deleted=False),
            **{k: v
               for k, v in request.GET.items()}
        }
        return render(request, self.template_name, context)


class CreateUpdateInvoiceView(PermissionRequiredMixin, View):
    template_name = "dashboard/accounting/invoices.html"
    permission_required = [
        "setup.view_dashboard",
        "setup.manage_accounting",
        "setup.add_invoice",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        context = {
            "sessions": SchoolSession.objects.filter(deleted=False),
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        name = request.POST.get("name")
        note = request.POST.get("note")
        session_id = request.POST.get("session")
        invoice_id = request.POST.get("invoice_id") or -1
        session = get_object_or_404(SchoolSession, id=session_id)
        invoice = Invoice.objects.filter(id=invoice_id).first()
        if not invoice:
            invoice = Invoice.objects.create(name=name,
                                             note=note,
                                             session=session,
                                             created_by=request.user,
                                             updated_by=request.user)
        else:
            invoice.name = name
            invoice.note = note
            invoice.session = session
            invoice.updated_by = request.user
            invoice.save()
        return redirect("dashboard:invoice_details", invoice_id=invoice.id)


class InvoiceDetailsView(PermissionRequiredMixin, View):
    template_name = "dashboard/accounting/invoice_details.html"
    permission_required = [
        "setup.view_dashboard",
        "setup.manage_accounting",
        "setup.add_invoice",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, invoice_id):
        invoice = get_object_or_404(Invoice, id=invoice_id)
        classes = Klass.objects.filter(deleted=False)
        context = {
            "invoice": invoice,
            "invoice_items": invoice.invoice_items.filter(deleted=False),
            "classes": classes,
            "sessions": SchoolSession.objects.filter(deleted=False),
        }
        context.update(make_model_key_value(invoice))
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request, invoice_id):
        invoice = get_object_or_404(Invoice, id=invoice_id)
        classes_ids = request.POST.getlist("classes")
        included_students = request.POST.get("included_students", "").replace(
            "\r", "").replace("\n", "").split(",")
        excluded_students = request.POST.get("excluded_students", "").replace(
            "\r", "").replace("\n", "").split(",")

        classes = Klass.objects.filter(id__in=classes_ids)
        students = Student.objects.filter(
            Q(klass__in=classes)
            | Q(student_id__in=included_students)).exclude(
                student_id__in=excluded_students)
        old_students = invoice.students.all()
        invoice.students.set(students)
        invoice.save()

        total_affected_student_ids = [
            student["student_id"]
            for student in students.union(old_students).values("student_id")
        ]
        # Trigger balance update.
        update_students_account.delay(total_affected_student_ids, invoice_id)
        messages.info(request,
                      "Students updated. Triggered for balance upates.")

        return redirect("dashboard:invoice_details", invoice_id=invoice.id)


class CreateUpdateInvoiceItem(PermissionRequiredMixin, View):
    template_name = "dashboard/accounting/edit_invoice_item.html"
    permission_required = [
        "setup.view_dashboard",
        "setup.manage_accounting",
        "setup.add_invoiceitem",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, invoice_id):
        invoice_item_id = request.GET.get("invoice_item_id")
        invoice_item = get_object_or_404(InvoiceItem, id=invoice_item_id)
        context = {
            "invoice_item": invoice_item,
            "invoice": invoice_item.invoice,
        }
        context.update(make_model_key_value(invoice_item))
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request, invoice_id):
        invoice = get_object_or_404(Invoice, id=invoice_id)
        invoice_item_id = request.POST.get("invoice_item_id") or -1
        invoice_item = InvoiceItem.objects.filter(id=invoice_item_id).first()
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        type = request.POST.get("type")

        invoice.status = InvoiceStatus.PENDING.value
        invoice.save()

        if not invoice_item:
            invoice_item = InvoiceItem.objects.create(invoice=invoice,
                                                      name=name,
                                                      amount=amount,
                                                      type=type,
                                                      created_by=request.user,
                                                      updated_by=request.user)
        else:
            invoice_item.name = name
            invoice_item.amount = amount
            invoice_item.type = type
            invoice_item.updated_by = request.user
            invoice_item.save()
        return redirect("dashboard:invoice_details", invoice_id=invoice.id)


class PaymentsView(PermissionRequiredMixin, View):
    template_name = "dashboard/accounting/payments.html"
    permission_required = [
        "setup.view_dashboard",
        "setup.manage_accounting",
        "setup.add_payment",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        query = request.GET.get("query")
        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")
        status = request.GET.get("status")
        transactions = Transaction.objects.all()
        if query:
            transactions = transactions.filter(
                Q(fullname__icontains=query) | Q(student__student_id=query))
        if status:
            transactions = transactions.filter(status__icontains=status)
        if from_date:
            transactions = transactions.filter(created_at__gte=from_date)
        if to_date:
            transactions = transactions.filter(created_at__lte=to_date)
        transactions = transactions.order_by("-created_at")

        context = {
            "transactions": transactions[:300],
            "sessions": SchoolSession.objects.filter(deleted=False),
            **{k: v
               for k, v in request.GET.items()}
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        student_id = request.POST.get("student_id")
        student = Student.objects.filter(student_id=student_id).first()
        if not student:
            messages.error(request,
                           f"Student with id: {student_id} not found.")
            return redirect(request.META.get("HTTP_REFERER"))
        return redirect("dashboard:create_update_payment",
                        student_id=student_id)


class CreateUpdatePayments(PermissionRequiredMixin, View):
    template_name = "dashboard/accounting/payment_detail.html"
    permission_required = [
        "setup.view_dashboard",
        "setup.manage_accounting",
        "setup.add_payment",
        "setup.change_payment",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, student_id):
        student = get_object_or_404(Student, student_id=student_id)
        context = {
            "student": student,
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request, student_id):
        student = get_object_or_404(Student, student_id=student_id)
        note = request.POST.get("note")
        amount = request.POST.get("amount")
        transaction = Transaction.objects.create(
            account=student.user.account,
            amount=amount,
            student=student,
            note=note,
            initiated_by=request.user,
            status="success",
            direction=TransactionDirection.IN.value,
            fullname=student.user.get_name(),
            status_message=TransactionStatusMessages.SUCCESS.value)
        transaction.update_account_balances()
        return redirect("dashboard:payments")


class BulkInvoiceGenerator(PermissionRequiredMixin, View):
    template_name = "pdf_processor/bulk-student-bill-sheet.html"
    permission_required = [
        "setup.view_dashboard",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, invoice_id):
        invoice = get_object_or_404(Invoice, id=invoice_id)
        name = ''.join(filter(str.isalnum, invoice.name.lower()))
        filename = f"{name}_{timezone.now().strftime('%y%m%d%H%M%S%f')}.pdf"

        task = generate_bulk_pdf_bill_sheet.delay(invoice_id, filename)

        return redirect("dashboard:bulk_bill_sheet_generation_status",
                        task.task_id, filename)


class GeneralReportStatusView(View):
    template_name = "dashboard/accounting/bulk_bill_sheet_generation_status.html"

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, task_id, filename):
        context = {
            "task_id": task_id,
            "filename": filename,
        }
        return render(request, self.template_name, context)


class StudentInvoicesView(PermissionRequiredMixin, View):
    template_name = "dashboard/accounting/student_invoices.html"
    permission_required = [
        "setup.manage_accounting",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, student_id):
        query = request.GET.get("query")
        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")

        student = get_object_or_404(Student, student_id=student_id)
        invoices = student.invoices.all()

        if query:
            invoices = invoices.filter(name__icontains=query)
        if from_date:
            invoices = invoices.filter(created_at__gte=from_date)
        if to_date:
            invoices = invoices.filter(created_at__lte=to_date)
        invoices = invoices.order_by("-created_at")
        context = {
            "invoices": invoices,
            "student": student,
            **{k: v
               for k, v in request.GET.items()}
        }
        return render(request, self.template_name, context)


class StudentInvoiceDetailView(PermissionRequiredMixin, View):
    template_name = "dashboard/accounting/student_invoice_details.html"
    permission_required = [
        "setup.manage_accounting",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, student_id, invoice_id):
        invoice = get_object_or_404(Invoice, id=invoice_id)
        context = {
            "invoice": invoice,
            "invoice_items": invoice.invoice_items.filter(deleted=False)
        }
        return render(request, self.template_name, context)
