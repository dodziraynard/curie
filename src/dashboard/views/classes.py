from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from dashboard.forms import ClassForm
from dashboard.mixins import CreateUpdateMixin
from dashboard.models import Course, Klass, Staff


class ClassesView(PermissionRequiredMixin, View):
    template_name = "dashboard/classes/classes.html"
    permission_required = [
        "dashboard.view_klass",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        classes = Klass.objects.all()
        courses = Course.objects.all()
        staff = Staff.objects.filter(user__is_active=True, has_left=False)
        context = {
            "classes": classes,
            "staff": staff,
            "courses": courses,
        }
        return render(request, self.template_name, context)


class CreateUpdateClassView(PermissionRequiredMixin, CreateUpdateMixin):
    template_name = "dashboard/classes/edit_class.html"
    form_class = ClassForm
    object_id_field = "id"
    model_class = Klass
    object_name = "class"
    redirect_url = "dashboard:classes"
    permission_required = (
        "dashboard.add_klass",
        "dashboard.change_klass",
    )

    def get_context_data(self):
        return {
            "staff": Staff.objects.filter(user__is_active=True,
                                          has_left=False),
            "courses": Course.objects.all(),
        }
