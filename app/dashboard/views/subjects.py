from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from dashboard.forms import SubjectForm
from dashboard.mixins import CreateUpdateMixin
from dashboard.models import Department, Subject


class SubjectsView(PermissionRequiredMixin, View):
    template_name = "dashboard/subjects/subjects.html"
    permission_required = [
        "setup.view_subject",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        subjects = Subject.objects.all()
        departments = Department.objects.all()
        context = {
            "subjects": subjects,
            "departments": departments,
        }
        return render(request, self.template_name, context)


class CreateUpdateSubjectView(PermissionRequiredMixin, CreateUpdateMixin):
    template_name = "dashboard/subjects/edit_subject.html"
    form_class = SubjectForm
    object_id_field = "subject_id"
    model_class = Subject
    object_name = "subject"
    redirect_url = "dashboard:subjects"
    permission_required = (
        "setup.add_subject",
        "setup.change_subject",
    )

    def get_context_data(self):
        return {
            "departments": Department.objects.all(),
        }