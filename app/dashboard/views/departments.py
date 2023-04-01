from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from dashboard.forms import DepartmentForm
from dashboard.mixins import CreateUpdateMixin
from dashboard.models import Department, Staff


class DepartmentsView(PermissionRequiredMixin, View):
    template_name = "dashboard/departments/departments.html"
    permission_required = [
        "dashboard.view_department",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        departments = Department.objects.all()
        staff = Staff.objects.filter(user__is_active=True)
        context = {
            "departments": departments,
            "staff": staff,
        }
        return render(request, self.template_name, context)


class CreateUpdateDepartmentView(PermissionRequiredMixin, CreateUpdateMixin):
    template_name = "dashboard/departments/edit_department.html"
    form_class = DepartmentForm
    object_id_field = "department_id"
    model_class = Department
    object_name = "department"
    redirect_url = "dashboard:departments"
    permission_required = (
        "dashboard.add_department",
        "dashboard.change_department",
    )

    def get_context_data(self):
        return {
            "staff": Staff.objects.filter(user__is_active=True),
        }
