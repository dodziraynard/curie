from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from dashboard.forms import CourseForm
from dashboard.mixins import CreateUpdateMixin
from dashboard.models import Course, Department, Subject


class CoursesView(PermissionRequiredMixin, View):
    template_name = "dashboard/courses/courses.html"
    permission_required = [
        "dashboard.view_course",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        courses = Course.objects.filter(deleted=False)
        subjects = Subject.objects.filter(deleted=False)
        departments = Department.objects.filter(deleted=False)
        context = {
            "courses": courses,
            "departments": departments,
            "subjects": subjects,
        }
        return render(request, self.template_name, context)


class CreateUpdateCourseView(PermissionRequiredMixin, CreateUpdateMixin):
    template_name = "dashboard/courses/edit_course.html"
    form_class = CourseForm
    object_id_field = "course_id"
    model_class = Course
    object_name = "course"
    redirect_url = "dashboard:courses"
    permission_required = (
        "dashboard.add_course",
        "dashboard.change_course",
    )

    def get_context_data(self):
        departments = Department.objects.filter(deleted=False)
        subjects = Subject.objects.filter(deleted=False)
        return {
            "subjects": subjects,
            "departments": departments,
        }
