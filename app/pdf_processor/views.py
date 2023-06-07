from collections import namedtuple

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import HttpResponse, get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from accounts.models import User

from dashboard.models import Record, SessionReport
from graphql_api.models.accounting import Invoice
from setup.models import GradingSystem, School, SchoolSession
from num2words import num2words

from .utils import render_to_pdf


class SingleAcademicRecordReportView(PermissionRequiredMixin, View):
    template_name = "pdf_processor/single-student-report.html"
    permission_required = [
        "setup.view_dashboard",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, session_id, student_id):
        session = get_object_or_404(SchoolSession, pk=session_id)
        records = Record.objects.filter(
            session=session,
            # klass__class_id=class_id,
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


class PersonalAcadmicReport(PermissionRequiredMixin, View):
    template_name = "pdf_processor/bulk-student-report.html"
    permission_required = [
        "setup.view_personal_academic_record",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        session_id = SchoolSession.objects.first().id or request.GET.get(
            "session")
        session = get_object_or_404(SchoolSession, pk=session_id)
        student_id = request.user.student.student_id
        records = Record.objects.filter(
            Q(session=session)
            | Q(session=session, student__student_id=student_id))

        session_reports = SessionReport.objects.filter(session=session)

        data = []

        # for student_id in student_ids:
        st_records = records.filter(student__student_id=student_id).order_by("subject__name")
        positions = st_records.values_list("position", flat=True)
        st_reports = session_reports.filter(
            student__student_id=student_id).first()
        average_pos = "N/A"
        if all(positions):
            average_pos = num2words(sum(positions) //
                                    max(st_records.count(), 1),
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
                average_pos = num2words(sum(positions) //
                                        max(st_records.count(), 1),
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


class PersonalTranscriptionView(PermissionRequiredMixin, View):
    template_name = "pdf_processor/blocks/transcript-ui.html"
    permission_required = [
        "setup.view_personal_academic_record",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        try:
            student_id = request.user.student.student_id
        except User.student.RelatedObjectDoesNotExist:
            return HttpResponse("No records found.")

        records = Record.objects.filter(student__student_id=student_id)

        session_ids = records.values_list("session", flat=True)
        sessions = SchoolSession.objects.filter(id__in=session_ids)
        data = []
        for session in sessions:
            session_records = records.filter(session=session)
            data.append((session, session_records))

        context = {
            "school": School.objects.first(),
            "data": data,
            "user": request.user,
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