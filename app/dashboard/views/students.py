from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models import Q
from dashboard.mixins import CreateUpdateMixin
from dashboard.models import (Course, House, Klass, Relative, Student, Subject,
                              Track)
from dashboard.utils.sheet_operations import insert_students
from lms.utils.functions import make_model_key_value

User = get_user_model()


class StudentsView(PermissionRequiredMixin, View):
    template_name = "dashboard/students/students.html"
    permission_required = [
        "dashboard.view_student",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        query = request.GET.get("query")
        class_id = request.GET.get("class_id")
        students = Student.objects.filter(deleted=False, completed=False).order_by("-created_at")
        courses = Course.objects.all().order_by("name")
        houses = House.objects.all().order_by("name")
        tracks = Track.objects.all().order_by("name")
        classes = Klass.objects.all().order_by("stage")
        subjects = Subject.objects.filter(is_elective=True)

        if query:
            students = students.filter(
                Q(student_id__icontains=query)
                | Q(user__surname__icontains=query)
                | Q(user__other_names__icontains=query))
        if class_id:
            students = students.filter(klass__id=class_id)

        context = {
            "students": students[:500],
            "houses": houses,
            "tracks": tracks,
            "courses": courses,
            "classes": classes,
            "subjects": subjects,
            **{k: v
               for k, v in request.GET.items()},
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
        courses = Course.objects.all().order_by("name")
        houses = House.objects.all().order_by("name")
        tracks = Track.objects.all().order_by("name")
        classes = Klass.objects.all().order_by("stage")
        subjects = Subject.objects.filter(is_elective=True)

        context = {
            "student": student,
            "houses": houses,
            "tracks": tracks,
            "courses": courses,
            "classes": classes,
            "subjects": subjects,
        }
        context.update(make_model_key_value(student.user))
        context.update(make_model_key_value(student))

        for relative in student.relatives.all():
            context.update({
                f"{relative.relationship}_" + k: v
                for k, v in make_model_key_value(relative).items()
            })
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        student_id = request.POST.get("id") or -1
        username = request.POST.get("student_id") or Student.generate_student_id()
        completed = bool(request.POST.get("completed", 0))
        electives = request.POST.getlist("elective_ids")
        electives = Subject.objects.filter(id__in=electives, is_elective=True)

        student = Student.objects.filter(id=student_id)
        
        if not username:
            messages.error(request, "Student ID is required.")
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
                messages.error(request, str(e))
                courses = Course.objects.all()
                houses = House.objects.all()
                tracks = House.objects.all()
                classes = Klass.objects.all()
                subjects = Subject.objects.filter(is_elective=True)

                context = {
                    "houses": houses,
                    "tracks": tracks,
                    "courses": courses,
                    "classes": classes,
                    "subjects": subjects,
                }
                context.update({k: v for k, v in request.POST.items()})
                return render(request, self.template_name, context)
        else:
            user = student.user

        for key, value in [*request.POST.items()]:
            if key in ["id", "student_id"]: continue
            if hasattr(student, key):
                setattr(student, key, value)
            elif hasattr(user, key):
                setattr(user, key, value)

        photo = request.FILES.get("photo")
        if photo:
            user.photo = photo

        user.phone = student.sms_number
        user.save()
        student.electives.set(electives)
        student.completed = completed
        student.save()

        # Process relatives
        relationships = ["father", "mother", "guardian"]
        student.relatives.clear()
        for relationship in relationships:
            relative_id = request.POST.get(relationship + "_relative_id",
                                           "") or -1
            fullname = request.POST.get(relationship + "_fullname")
            phone = request.POST.get(relationship + "_phone")
            occupation = request.POST.get(relationship + "_occupation")
            address = request.POST.get(relationship + "_address")

            relative = Relative.objects.filter(id=relative_id).first()

            if not relative:
                relative = Relative.objects.create(relationship=relationship)
            if fullname:
                relative.fullname = fullname
            if phone:
                relative.phone = phone
            if occupation:
                relative.occupation = occupation
            if relationship:
                relative.relationship = relationship
            if address:
                relative.address = address
            relative.save()

            student.relatives.add(relative)
            student.save()
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
