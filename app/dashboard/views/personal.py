from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from accounts.models import User
from dashboard.models import Record
from graphql_api.models.accounting import Invoice
from setup.models import SchoolSession


class PesonalAcademicRecord(PermissionRequiredMixin, View):
    template_name = "dashboard/personal/academic_record.html"
    permission_required = [
        "setup.view_personal_academic_record",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        session_ids = Record.objects.filter(
            student__user=request.user).values_list("session", flat=True)
        sessions = SchoolSession.objects.filter(id__in=session_ids).distinct()
        context = {
            "sessions": sessions,
        }
        return render(request, self.template_name, context)


class MyInvoicesView(PermissionRequiredMixin, View):
    template_name = "dashboard/personal/invoices.html"
    permission_required = [
        "setup.view_personal_invoice",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        query = request.GET.get("query")
        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")

        try:
            invoices = request.user.student.invoices.all()
        except User.student.RelatedObjectDoesNotExist:
            raise Http404

        if query:
            invoices = invoices.filter(name__icontains=query)
        if from_date:
            invoices = invoices.filter(created_at__gte=from_date)
        if to_date:
            invoices = invoices.filter(created_at__lte=to_date)
        invoices = invoices.order_by("-created_at")
        context = {
            "invoices": invoices,
            **{k: v
               for k, v in request.GET.items()}
        }
        return render(request, self.template_name, context)


class MyInvoiceDetailView(PermissionRequiredMixin, View):
    template_name = "dashboard/personal/invoice_details.html"
    permission_required = [
        "setup.view_personal_invoice",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, invoice_id):
        try:
            invoice = request.user.student.invoices.filter(
                id=invoice_id).first()
        except User.student.RelatedObjectDoesNotExist:
            raise Http404

        if not invoice:
            raise Http404

        context = {
            "invoice": invoice,
        }
        return render(request, self.template_name, context)


class PersonalPaymentHistory(PermissionRequiredMixin, View):
    template_name = "dashboard/personal/payment_history.html"
    permission_required = [
        "setup.view_personal_payment_history",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):

        context = {}
        return render(request, self.template_name, context)
