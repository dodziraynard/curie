from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from dashboard.models import SubjectMapping

from dashboard.models import Klass
from setup.models import SchoolSession


class ReportingIndexView(PermissionRequiredMixin, View):
    template_name = "dashboard/reporting/index.html"
    permission_required = [
        "setup.view_reporting",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        sessions = SchoolSession.objects.all()
        classes = Klass.objects.all()

        sessions = SchoolSession.objects.all().order_by("-start_date")
        classes = Klass.objects.all()
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
        sessions = SchoolSession.objects.all()
        classes = Klass.objects.all()

        context = {
            "sessions": sessions,
            "classes": classes,
        }
        return render(request, self.template_name, context)
