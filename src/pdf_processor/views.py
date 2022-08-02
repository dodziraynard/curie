from django.shortcuts import HttpResponse, get_object_or_404
from django.utils import timezone
from django.views import View
from dashboard.models import SessionReport, Record, Klass
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from setup.models import School, SchoolSession
from .utils import render_to_pdf


class SingleAcademicRecordReportView(PermissionRequiredMixin, View):
    template_name = "pdf_processor/single-student-report.html"
    permission_required = [
        "dashboard.view_dashboard",
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
        "dashboard.view_dashboard",
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
        "dashboard.view_dashboard",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        session_id = request.GET.get("session")
        classes = request.GET.getlist("classes")
        session = get_object_or_404(SchoolSession, pk=session_id)
        records = Record.objects.filter(session=session, klass_id__in=classes)

        student_ids = set(records.values_list("student__student_id",
                                              flat=True))

        session_reports = SessionReport.objects.filter(session=session)

        data = [
            (records.filter(student__student_id=student_id),
             session_reports.filter(student__student_id=student_id).first())
            for student_id in student_ids
        ]

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
