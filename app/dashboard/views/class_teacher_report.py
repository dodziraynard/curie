from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from dashboard.models import Klass, SessionReport, StudentPromotionHistory
from setup.models import Attitude, Conduct, Interest, Remark, SchoolSession


class ClassTeacherSessionReportFilterView(PermissionRequiredMixin, View):
    template_name = "dashboard/class_teacher_report/report_filter.html"
    permission_required = [
        "setup.change_class_teacher_remark",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        sessions = SchoolSession.objects.all().order_by("-start_date")

        if not request.user.has_perm("setup.manage_other_report"):
            if hasattr(request.user, "staff"):
                classes = request.user.staff.classes.all()
            else:
                classes = Klass.objects.none()
        else:
            classes = Klass.objects.all()

        context = {
            "sessions": sessions,
            "classes": classes,
        }
        return render(request, self.template_name, context)


class ClassTeacherSessionReportDataView(PermissionRequiredMixin, View):
    template_name = "dashboard/class_teacher_report/class_teacher_report_data.html"
    permission_required = [
        "setup.change_class_teacher_remark",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        session_id = request.GET.get("session") or -1
        class_id = request.GET.get("class") or -1
        session = SchoolSession.objects.filter(id=session_id).first()
        klass = Klass.objects.filter(id=class_id).first()

        if not (klass and session):
            messages.error(request, "Please select a session and class")
            return redirect("dashboard:class_teacher_report_filter")

        promotion_history = StudentPromotionHistory.objects.filter(
            session=session, new_class=klass)
        students = promotion_history.values_list("student", flat=True)

        for student_id in students:
            SessionReport.objects.get_or_create(student_id=student_id,
                                                klass=klass,
                                                session=session)

        reports = SessionReport.objects.filter(student__in=students,
                                               klass=klass,
                                               session=session)
        context = {
            "reports": reports,
            "session": session,
            "class": klass,
            "attitudes": Attitude.objects.all(),
            "interests": Interest.objects.all(),
            "conducts": Conduct.objects.all(),
            "remarks": Remark.objects.all(),
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        total_attendance = request.POST.get("total_attendance")
        report_ids = request.POST.getlist("report_ids")
        attendance_list = request.POST.getlist("attendance")
        attitudes = request.POST.getlist("attitudes")
        interests = request.POST.getlist("interests")
        conducts = request.POST.getlist("conducts")
        remarks = request.POST.getlist("remarks")
        classes = request.POST.getlist("classes")
        promotions = request.POST.getlist("promotions")

        # Validating user input
        if not (str(total_attendance).isdigit()):
            messages.error(request, "Invalid total attendance.")
            return redirect(request.META.get("HTTP_REFERER"))

        if len(attendance_list) != len(attitudes) != len(conducts) != len(
                report_ids) != len(classes) != len(promotions) != len(
                    remarks) != len(interests):
            messages.warning(
                request,
                "Invalid record. Please do not leave any records half filled.")
            return redirect(request.META.get("HTTP_REFERER"))

        # Check class teacher permissions
        has_class_teacher_permission = True
        class_ids = set(classes)
        teacher_klasses = Klass.objects.filter(
            id__in=class_ids, class_teacher__user=request.user)
        if len(teacher_klasses) != len(class_ids):
            has_class_teacher_permission = False

        # Updating records
        for report_id, class_id, attendance, attitude, conduct, interest, remark, promotion in zip(
                report_ids, classes, attendance_list, attitudes, conducts,
                interests, remarks, promotions):

            report = get_object_or_404(SessionReport, id=report_id)
            klass = get_object_or_404(Klass, id=class_id)

            # Check whether user has the permission to modify this record.
            if not (request.user.has_perm("setup.manage_other_report")
                    or has_class_teacher_permission
                    ):  # Administrative permission.
                messages.error(
                    request,
                    "You do not have permission to view or modify this subject record."
                )
                return redirect(request.META.get("HTTP_REFERER"))

            # Updating record
            report.total_attendance = total_attendance
            report.attendance = attendance
            report.klass = klass
            report.attitude_id = attitude
            report.conduct_id = conduct
            report.interest_id = interest
            report.promotion = promotion
            report.class_teacher_remark_id = remark
            report.save()

        messages.success(request, "Record successfully updated.")
        return redirect(request.META.get("HTTP_REFERER"))
