from collections import namedtuple

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import HttpResponse, get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View

from dashboard.models import Record, SessionReport
from graphql_api.models.accounting import Invoice
from setup.models import School, SchoolSession
from num2words import num2words

from .utils import render_to_pdf


class SingleAcademicRecordReportView(PermissionRequiredMixin, View):
    template_name = "pdf_processor/single-student-report.html"
    permission_required = [
        "setup.view_dashboard",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, session_id, class_id, student_id):
        session = get_object_or_404(SchoolSession, pk=session_id)
        records = Record.objects.filter(session=session,
                                        klass__class_id=class_id,
                                        student__student_id=student_id)

        session_report = SessionReport.objects.filter(
            session=session, student__student_id=student_id).first()
        context = {
            "session": session,
            "session_report": session_report,
            "school": School.objects.first(),
            "records": records,
            "current_time": timezone.now(),
        }

        pdf = render_to_pdf(self.template_name, context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Student-Report-Sheet.pdf"
            content = "inline; filename=%s" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename=%s" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found", status=404)


class StudentFullReportView(PermissionRequiredMixin, View):
    template_name = "pdf_processor/report_per_session.html"
    permission_required = [
        "setup.view_dashboard",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, student_id):
        records = Record.objects.filter(student__student_id=student_id)

        reports = {}
        context = {
            "reports": reports,
            "school": School.objects.first(),
            "records": records,
            "current_time": timezone.now(),
        }

        pdf = render_to_pdf(self.template_name, context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Student-Report-Sheet.pdf"
            content = "inline; filename=%s" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename=%s" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found", status=404)


class BulkAcademicRecordReportView(PermissionRequiredMixin, View):
    template_name = "pdf_processor/bulk-student-report.html"
    permission_required = [
        "setup.view_dashboard",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        session_id = request.GET.get("session")
        classes = request.GET.getlist("classes")
        student_ids = request.GET.get("student_ids").replace(" ",
                                                             "").split(",")
        session = get_object_or_404(SchoolSession, pk=session_id)
        records = Record.objects.filter(
            Q(session=session, klass_id__in=classes)
            | Q(session=session, student__student_id__in=student_ids))

        student_ids = set(records.values_list("student__student_id",
                                              flat=True))

        session_reports = SessionReport.objects.filter(session=session)

        data = []

        for student_id in student_ids:
            st_records = records.filter(student__student_id=student_id)
            positions = st_records.values_list("position", flat=True)
            st_reports = session_reports.filter(
                student__student_id=student_id).first()
            average_pos = "N/A"
            if all(positions):
                average_pos = num2words(sum(positions) // st_records.count(),
                                        to="ordinal_num")
            data.append((st_records, st_reports, average_pos))

        context = {
            "session": session,
            "school": School.objects.first(),
            "data": data,
            "current_time": timezone.now(),
        }

        pdf = render_to_pdf(self.template_name, context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Bulk-Student-Report-Sheet.pdf"
            content = "inline; filename=%s" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename=%s" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found", status=404)


class BulkStudentBillSheet(PermissionRequiredMixin, View):
    template_name = "pdf_processor/bulk-student-bill-sheet.html"
    permission_required = [
        "setup.view_dashboard",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, invoice_id):
        invoice = get_object_or_404(Invoice, id=invoice_id)

        records = []
        data = []
        total = invoice.total_amount
        Statement = namedtuple("Statement", "name type amount")
        for item in invoice.invoice_items.all():
            statement = Statement(item.name, item.type, item.amount)
            data.append(statement)

        for student in invoice.students.all():
            arears = round(total - float(student.user.account.amount_payable),
                           2) * -1
            records.append([student, total, arears, data[::]])

        context = {
            "session": invoice.session,
            "school": School.objects.first(),
            "records": records,
            "current_time": timezone.now(),
        }

        pdf = render_to_pdf(self.template_name, context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Bulk-Student-Report-Sheet.pdf"
            content = "inline; filename=%s" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename=%s" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found", status=404)
