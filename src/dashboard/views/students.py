from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class StudentsView(PermissionRequiredMixin, View):
    template_name = "dashboard/students/students.html"
    permission_required = [
        "dashboard.view_student",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        return render(request, self.template_name)
