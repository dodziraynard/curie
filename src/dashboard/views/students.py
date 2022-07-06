from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.views import View


class StudentsView(PermissionRequiredMixin, View):
    template_name = "dashboard/students/students.html"
    permission_required = [
        "dashboard.view_student",
    ]

    def get(self, request):
        return render(request, self.template_name)
