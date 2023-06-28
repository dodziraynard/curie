from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from dashboard.models.models import SubjectMapping

from dashboard.models import Klass
from pdf_processor.tasks import generate_bulk_pdf_report
from setup.models import SchoolSession
from django.utils import timezone


class ReportingIndexView(PermissionRequiredMixin, View):
    template_name = "dashboard/reporting/index.html"
    permission_required = [
        "setup.view_reporting",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        classes = Klass.objects.filter(deleted=False).order_by("name")

        sessions = SchoolSession.objects.all().order_by("-start_date")
        if not request.user.has_perm("setup.manage_other_report"):
            staff = request.user.staff if hasattr(request.user,
                                                  "staff") else None
            mappings = SubjectMapping.objects.filter(staff=staff)
            session_ids = mappings.values_list("session", flat=True)
            class_ids = mappings.values_list("klass", flat=True)

            sessions = sessions.filter(id__in=session_ids).distinct()
            classes = classes.filter(id__in=class_ids).distinct()

        context = {
            "sessions": sessions,
            "classes": classes,
        }
        return render(request, self.template_name, context)


class StudentFullReportView(PermissionRequiredMixin, View):
    template_name = "dashboard/reporting/student-full-report.html"
    permission_required = [
        "setup.view_reporting",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        sessions = SchoolSession.objects.filter(deleted=False).order_by("name")
        classes = Klass.objects.filter(deleted=False).order_by("name")

        context = {
            "sessions": sessions,
            "classes": classes,
        }
        return render(request, self.template_name, context)


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

        name = ''.join(filter(str.isalnum, session.name.lower()))
        filename = f"{name}_{timezone.now().strftime('%y%m%d%H%M%S%f')}.pdf"

        task = generate_bulk_pdf_report.delay(session_id=session_id,
                                              classes=classes,
                                              student_ids=student_ids,
                                              filename=filename)

        return redirect("dashboard:bulk_report_sheet_generation_status",
                        task.task_id, filename)


class StudentReportGenerationStatusView(View):
    template_name = "dashboard/reporting/bulk_report_sheet_generation_status.html"

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request, task_id, filename):
        context = {
            "task_id": task_id,
            "filename": filename,
        }
        return render(request, self.template_name, context)
