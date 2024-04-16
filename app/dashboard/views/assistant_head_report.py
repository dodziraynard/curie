from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from dashboard.models import SessionReport, StudentPromotionHistory
from setup.models import SchoolSession


class AssistantHeadSessionReportFilterView(PermissionRequiredMixin, View):
    template_name = "dashboard/assistant_head_report/report_filter.html"
    permission_required = [
        "setup.append_signature",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        sessions = SchoolSession.objects.all().order_by("-start_date")

        context = {
            "sessions": sessions,
        }
        return render(request, self.template_name, context)


class AssistantHeadSessionReportDataView(PermissionRequiredMixin, View):
    template_name = "dashboard/assistant_head_report/assistant_head_report_data.html"
    permission_required = [
        "setup.append_signature",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        session_id = request.GET.get("session") or -1
        session = SchoolSession.objects.filter(id=session_id).first()

        if not session:
            messages.error(request, "Session not found")
            return redirect("dashboard:assistant_head_report_filter")

        promotion_history = StudentPromotionHistory.objects.filter(
            session__academic_year=session.academic_year)
        students = promotion_history.values_list("student", flat=True)

        for student_id in students:
            try:
                SessionReport.objects.get_or_create(student_id=student_id,
                                                    deleted=False,
                                                    session=session)
            except Exception as _:
                SessionReport.objects.filter(student_id=student_id,
                                             deleted=False,
                                             session=session).delete()

        reports = SessionReport.objects.filter(student__in=students,
                                               deleted=False,
                                               student__completed=False,
                                               session=session).order_by("klass", "student__user__surname")
        context = {
            "reports": reports,
            "session": session,
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        session_id = request.GET.get("session") or -1
        session = SchoolSession.objects.filter(id=session_id).first()

        if not session:
            messages.error(request, "Session not found")
            return redirect("dashboard:assistant_head_report_filter")

        promotion_history = StudentPromotionHistory.objects.filter(
            session__academic_year=session.academic_year)
        students = promotion_history.values_list("student", flat=True)

        for student_id in students:
            SessionReport.objects.get_or_create(student_id=student_id,
                                                deleted=False,
                                                session=session)

        reports = SessionReport.objects.filter(student__in=students,
                                               deleted=False,
                                               session=session)
        for report in reports:
            report.assistant_head_signature = request.user.signature
            report.save()

        messages.success(request, "Record successfully signed.")
        return redirect(request.META.get("HTTP_REFERER"))
