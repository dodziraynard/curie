from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages

from dashboard.mixins import CreateUpdateMixin
from dashboard.models import Course, House, Klass, Student, Subject
from django.core.exceptions import ValidationError
from dashboard.utils.sheet_operations import insert_students

from lms.utils.functions import make_model_key_value
from django.contrib.auth import get_user_model

User = get_user_model()


class StudentsView(PermissionRequiredMixin, View):
    template_name = "dashboard/students/students.html"
    permission_required = [
        "dashboard.view_student",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        students = Student.objects.all()
        courses = Course.objects.all()
        houses = House.objects.all()
        tracks = House.objects.all()
        classes = Klass.objects.all()
        subjects = Subject.objects.all()

        context = {
            "students": students,
            "houses": houses,
            "tracks": tracks,
            "courses": courses,
            "classes": classes,
            "subjects": subjects,
        }
        return render(request, self.template_name, context)


class CreateUpdateStudentView(PermissionRequiredMixin, CreateUpdateMixin):
    template_name = "dashboard/students/edit_student.html"
    permission_required = [
        "dashboard.add_student",
        "dashboard.change_student",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        student_id = request.GET.get("id") or -1
        student = get_object_or_404(Student, id=student_id)

        courses = Course.objects.all()
        houses = House.objects.all()
        tracks = House.objects.all()
        classes = Klass.objects.all()
        subjects = Subject.objects.all()

        context = {
            "student": student,
            "houses": houses,
            "tracks": tracks,
            "courses": courses,
            "classes": classes,
            "subjects": subjects,
        }
        context.update(make_model_key_value(student))
        context.update(make_model_key_value(student.user))
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        student_id = request.POST.get("id") or -1
        username = request.POST.get("student_id")
        electives = request.POST.getlist("elective_ids")
        electives = Subject.objects.filter(id__in=electives, is_elective=True)

        student = Student.objects.filter(id=student_id)

        if not username:
            messages.error(request, "Username is required.")
            return redirect(
                request.META.get("HTTP_REFERER") or "dashboard:index")

        student = Student.objects.filter(id=student_id).first()
        if not student:
            user, _ = User.objects.get_or_create(username=username)
            user.set_password(user.temporal_pin)
            user.save()
            try:
                student, _ = Student.objects.get_or_create(student_id=username,
                                                           user=user)
            except ValidationError as e:
                messages.error(request, e.message)
                return redirect(
                    request.META.get("HTTP_REFERER") or "dashboard:index")
        else:
            user = student.user
        for key, value in [*request.POST.items(), *request.FILES.items()]:
            if key in ["id"]: continue
            if hasattr(student, key):
                setattr(student, key, value)
            elif hasattr(user, key):
                setattr(user, key, value)

        user.save()
        student.electives.set(electives)
        student.save()
        return redirect(request.META.get("HTTP_REFERER") or "dashboard:index")


class AddBulkStudents(PermissionRequiredMixin, View):
    template_name = "dashboard/students/add_bulk_students.html"
    permission_required = [
        "dashboard.add_student",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        context = {}
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        file = request.FILES.get("file")
        result = insert_students(file.file)
        context = {
            "error_messages": result,
        }
        if not result:
            messages.success(request, "Students added successfully.")
        return render(request, self.template_name, context)
