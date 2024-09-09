import bisect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import HttpResponse, get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from accounts.models import User
from django.db.models import Sum

from dashboard.models import Record, SessionReport, Student, StudentPromotionHistory
from setup.models import School, SchoolSession
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
        student = get_object_or_404(Student, student_id=student_id)
        records = Record.objects.filter(deleted=False).filter(
            session=session, deleted=False,
            student__student_id=student_id).order_by("subject__name")

        session_report = SessionReport.objects.filter(
            deleted=False, session=session,
            student__student_id=student_id).first()
        klass = StudentPromotionHistory.get_class(student, session)

        average_position = "N/A"
        results = Record.objects.filter(klass=klass, deleted=False).exclude(
            total=None).values('student__student_id').annotate(
                total_record=Sum('total'))
        totals = sorted([-record["total_record"] for record in results])
        for result in results:
            if result.get("student__student_id") == student_id:
                pos = bisect.bisect_left(totals,
                                         -result.get("total_record")) + 1
                average_position = num2words(pos, to="ordinal_num")
                break

        context = {
            "session": session,
            "session_report": session_report,
            "school": School.objects.first(),
            "records": records,
            "average_position": average_position,
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
        session_id = request.GET.get(
            "session") or SchoolSession.objects.first().id
        session = get_object_or_404(SchoolSession, pk=session_id)
        try:
            student_id = request.user.student.student_id
            klass = StudentPromotionHistory.get_class(request.user.student,
                                                      session)
        except User.student.RelatedObjectDoesNotExist:
            raise Http404()

        if not klass:
            return HttpResponse(f"No record found for class {klass}",
                                status=404)

        st_records = Record.objects.filter(deleted=False).filter(
            session=session, klass=klass,
            student__student_id=student_id).order_by("subject__name")

        session_reports = SessionReport.objects.filter(session=session)

        data = []

        average_pos = "N/A"
        results = Record.objects.filter(
            klass=klass, session=session, deleted=False).exclude(
                total=None).values('student__student_id').annotate(
                    total_record=Sum('total')).order_by("-total_record")
        totals = sorted([-record["total_record"] for record in results])
        for result in results:
            if result.get("student__student_id") == student_id:
                pos = bisect.bisect_left(totals,
                                         -result.get("total_record")) + 1
                average_pos = num2words(pos, to="ordinal_num")
                break

        st_reports = session_reports.filter(
            student__student_id=student_id).first()
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
        records = Record.objects.filter(deleted=False).filter(
            Q(session=session, klass_id__in=classes)
            | Q(session=session, student__student_id__in=student_ids))

        student_ids = set(records.values_list("student__student_id",
                                              flat=True))

        session_reports = SessionReport.objects.filter(session=session)

        data = []

        for student_id in student_ids:
            student = Student.objects.filter(student_id=student_id).first()
            st_records = records.filter(student__student_id=student_id)
            st_reports = session_reports.filter(
                student__student_id=student_id).first()

            average_pos = "N/A"
            klass = StudentPromotionHistory.get_class(student, session)
            results = records.objects.filter(
                klass=klass, deleted=False).exclude(
                    total=None).values('student__student_id').annotate(
                        total_record=Sum('total')).order_by("-total_record")
            totals = sorted([-record["total_record"] for record in results])
            for result in results:
                if result.get("student__student_id") == student_id:
                    pos = bisect.bisect_left(totals,
                                             -result.get("total_record")) + 1
                    average_pos = num2words(pos, to="ordinal_num")
                    break

            data.append((st_records, st_reports, average_pos))

        data.sort(key=lambda item: item[0].first().klass.stage)

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

        records = Record.objects.filter(deleted=False).filter(
            student__student_id=student_id)

        session_ids = records.values_list("session", flat=True)
        sessions = SchoolSession.objects.filter(
            id__in=session_ids).order_by("-next_start_date")
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
