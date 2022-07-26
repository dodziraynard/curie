from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from dashboard.models import Klass
from setup.models import SchoolSession


class ReportingIndexView(PermissionRequiredMixin, View):
    template_name = "dashboard/reporting/index.html"
    permission_required = [
        "dashboard.view_dashboard",
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
