from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import get_user_model
from dashboard.models import Klass, Staff, Student, Subject, SubjectMapping

from setup.models import School, SchoolSession

User = get_user_model()


class ActionCenterView(PermissionRequiredMixin, View):
    template_name = "dashboard/action_center/index.html"
    permission_required = [
        "dashboard.view_dashboard",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class SubjectMappingView(PermissionRequiredMixin, View):
    template_name = "dashboard/action_center/subject_mapping.html"
    permission_required = [
        "dashboard.view_dashboard",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        session_id = request.GET.get("session_id") or -1

        sessions = SchoolSession.objects.all().order_by("-start_date")
        classes = Klass.objects.all()
        subjects = Subject.objects.filter(is_elective=False)
        teachers = Staff.objects.all()

        current_session = SchoolSession.objects.filter(id=session_id).first(
        ) or School.objects.first().get_current_session()

        for class_ in classes:
            subjects = subjects.union(class_.course.subjects.all())
            for subject in subjects:
                mapping, created = SubjectMapping.objects.get_or_create(
                    klass=class_, subject=subject, session=current_session)
                if created:
                    previous_mapping = SubjectMapping.objects.filter(
                        klass=class_, subject=subject).exclude(
                            session=current_session).order_by(
                                "-created_at").first()
                    if previous_mapping:
                        mapping.staff = previous_mapping.staff
                        mapping.save()

        mappings = SubjectMapping.objects.filter(session=current_session)
        context = {
            "sessions": sessions,
            "mappings": mappings.order_by("subject__name", "klass__name"),
            "teachers": teachers
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        mappings = request.POST.getlist("mappings")
        if not mappings:
            messages.error(request, "No mappings selected")
            return redirect("dashboard:subject_mapping")

        _, _, session, _ = mappings[0].split("|")
        session = SchoolSession.objects.get(id=session)

        if not (session and session.active()):
            messages.error(request, "Session is not active")
            return redirect(request.META.get("HTTP_REFERER"))

        for mapping in mappings:
            split = mapping.split("|")
            if len(split) != 4:
                messages.error(request, "Invalid mapping")
                return redirect(request.META.get("HTTP_REFERER"))
            klass, subject, session, staff = split
            subject_mapping = SubjectMapping.objects.filter(
                klass_id=klass, subject_id=subject,
                session_id=session).first()
            if subject_mapping:
                subject_mapping.staff_id = staff
                subject_mapping.save()
            else:
                messages.error(request, "Invalid mapping")
        return redirect(request.META.get("HTTP_REFERER"))


class StudentPromotionView(PermissionRequiredMixin, View):
    template_name = "dashboard/action_center/student_promotion.html"
    permission_required = [
        "dashboard.view_dashboard",
        "dashboard.promote_student",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        context = {}
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        exceptions = request.POST.get("exceptions", "")
        step = request.POST.get("step")
        if not (step and step.lstrip("-").isdigit()):
            messages.error(request, "Invalid step")
            return redirect(request.META.get("HTTP_REFERER"))
        step = int(step)

        exceptions = exceptions.replace(" ", "").split(",")
        students = Student.objects.exclude(student_id__in=exceptions)

        failures = False
        count = 0
        for student in students:
            res = student.promote(step)
            if all(res):
                count += 1
            elif not any(res):
                failures = True
        if failures:
            messages.warning(
                request, "Suitable classes were not found for some students.")
        else:
            messages.success(request,
                             f"{count} students promoted successfully")

        return redirect(request.META.get("HTTP_REFERER"))
