from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from dashboard.models import Klass, Record, Staff, Student, StudentPromotionHistory, Subject, SubjectMapping
from lms.utils.functions import get_current_session
from django.db.utils import NotSupportedError
import logging

from setup.models import School, SchoolSession

logger = logging.getLogger("system")


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
        session = get_current_session()
        promotion_exists = StudentPromotionHistory.objects.filter(
            session=session).exists()

        promotion_sessions = set(
            StudentPromotionHistory.objects.all().order_by(
                "-created_at").values_list("session", flat=True))

        promotion_histories = []
        for session_id in promotion_sessions:
            session = SchoolSession.objects.get(id=session_id)
            history = StudentPromotionHistory.objects.filter(session=session)
            promotion_histories.append({
                "session":
                session,
                "students_count":
                history.values("student").distinct().count(),
                "classes_count":
                history.values("new_class").distinct().count(),
            })
        context = {
            "promotion_exists": promotion_exists,
            "promotion_histories": promotion_histories,
        }
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


class RevertPromotionView(PermissionRequiredMixin, View):
    permission_required = [
        "dashboard.view_dashboard",
        "dashboard.promote_student",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        return redirect("dashboard:student_promotion")

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        session_id = request.POST.get("session_id") or -1
        session = SchoolSession.objects.get(id=session_id)
        if not session:
            messages.error(request, "No session selected")
            return redirect(request.META.get("HTTP_REFERER"))
        histories = StudentPromotionHistory.objects.filter(session=session)
        for history in histories:
            if history.old_class and history.new_class and history.new_class != history.old_class:
                # This is not an initial promotion
                history.student.klass = history.old_class
                history.student.completed = False
                history.student.save()
                history.delete()

        messages.success(request, "Promotion has been reverted.")
        return redirect(request.META.get("HTTP_REFERER"))


class AcademicRecordSelectionView(PermissionRequiredMixin, View):
    template_name = "dashboard/action_center/academic_record_selection.html"

    permission_required = []

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        sessions = SchoolSession.objects.all().order_by("-start_date")
        classes = Klass.objects.all()
        subjects = Subject.objects.all()
        context = {
            "sessions": sessions,
            "classes": classes,
            "subjects": subjects
        }
        return render(request, self.template_name, context)


class AcademicRecordDataView(PermissionRequiredMixin, View):
    template_name = "dashboard/action_center/academic_record_data.html"

    permission_required = []

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        session = request.GET.get("session")
        subject = request.GET.get("subject")
        classes = request.GET.getlist("classes")

        if not (session and subject):
            messages.error(request, "Please choose a session and a subject")
            return redirect("dashboard:academic_record_selection")

        session = get_object_or_404(SchoolSession, id=session)
        subject = get_object_or_404(Subject, id=subject)
        classes = Klass.objects.filter(id__in=classes)

        students = Student.objects.filter(start_date__lte=session.start_date,
                                          end_date__gte=session.end_date)
        if classes:
            students = students.filter(klass__in=classes)
        if subject.is_elective:
            students = students.filter(electives=subject)

        # Validate user
        if not request.user.has_perm("dashboard.manage_other_record"):
            mappings = SubjectMapping.objects.filter(
                session=session,
                staff__user_id=request.user.id,
                subject=subject)
            for klass in classes:
                if not mappings.filter(klass=klass).exists():
                    error_message = f"You do not have permission to view or modify records of {subject.name} in {klass.name} for {session.name}"
                    messages.error(request, error_message)
                    return redirect(request.META.get("HTTP_REFERER"))

        # Get the academic records for the selected classes
        for student in students:
            record, created = Record.objects.get_or_create(student=student,
                                                           subject=subject,
                                                           session=session)
            if created:
                record.klass = student.klass
                record.save()

        records = Record.objects.filter(
            session=session, student__in=students,
            subject=subject).order_by("student__user__surname")

        context = {
            "records": records,
            "session": session,
            "subject": subject,
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        total_class_score = request.POST.get("total_class_score") or 100
        total_exam_score = request.POST.get("total_exam_score") or 100
        session = request.POST.get("session")
        subject = request.POST.get("subject")
        class_scores = request.POST.getlist("class_scores")
        exam_scores = request.POST.getlist("exam_scores")
        record_ids = request.POST.getlist("record_ids")
        classes = request.POST.getlist("classes")

        # Validating user input
        if not (str(total_class_score).isdigit()
                and str(total_exam_score).isdigit()):
            messages.error(request, "Invalid total scores")
            return redirect(request.META.get("HTTP_REFERER"))

        if not (session and subject):
            messages.error(request, "Please choose a session and a subject")
            return redirect(request.META.get("HTTP_REFERER"))

        if len(class_scores) != len(exam_scores) != len(record_ids) != len(
                classes):
            messages.error(request, "Invalid scores")
            return redirect(request.META.get("HTTP_REFERER"))

        session = get_object_or_404(SchoolSession, id=session)
        subject = get_object_or_404(Subject, id=subject)

        # Get the user's (teacher's) assigned classes and subjects.
        mappings = SubjectMapping.objects.filter(
            session=session, staff__user_id=request.user.id, subject=subject)

        # Updating records
        for record_id, class_id, class_score, exam_score in zip(
                record_ids, classes, class_scores, exam_scores):
            record = get_object_or_404(Record, id=record_id)
            klass = get_object_or_404(Klass, id=class_id)

            # Check whether user has the permission to modify this record.
            if not request.user.has_perm("dashboard.manage_other_record"
                                         ):  # Administrative permission.
                if not mappings.filter(klass=record.klass).exists():
                    messages.error(
                        request,
                        "You do not have permission to view or modify this subject record."
                    )
                    return redirect(request.META.get("HTTP_REFERER"))

            record.total_class_score = int(total_class_score)
            record.total_exam_score = int(total_exam_score)
            record.class_score = int(class_score)
            record.exam_score = int(exam_score)
            record.klass = klass
            record.updated_by = request.user
            record.save()

        messages.success(request, "Scores updated successfully")
        return redirect(request.META.get("HTTP_REFERER"))
