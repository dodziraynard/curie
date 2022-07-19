from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from dashboard.models import House, SessionReport, StudentPromotionHistory

from setup.models import Remark, SchoolSession


class HouseMasterSessionReportFilterView(PermissionRequiredMixin, View):
    template_name = "dashboard/house_master_report/report_filter.html"
    permission_required = [
        "dashboard.view_dashboard",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        sessions = SchoolSession.objects.all().order_by("-start_date")
        houses = House.objects.all()

        context = {
            "sessions": sessions,
            "houses": houses,
        }
        return render(request, self.template_name, context)


class HouseMasterSessionReportDataView(PermissionRequiredMixin, View):
    template_name = "dashboard/house_master_report/house_master_report_data.html"
    permission_required = [
        "dashboard.view_dashboard",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        session_id = request.GET.get("session") or -1
        house_id = request.GET.get("house") or -1
        session = SchoolSession.objects.filter(id=session_id).first()
        house = House.objects.filter(id=house_id).first()

        if not (house and session):
            messages.error(request, "Please select a session and class")
            return redirect("dashboard:house_master_report_filter")

        promotion_history = StudentPromotionHistory.objects.filter(
            student__house=house, session=session)
        students = promotion_history.values_list("student", flat=True)

        for student_id in students:
            SessionReport.objects.get_or_create(student_id=student_id,
                                                session=session)

        reports = SessionReport.objects.filter(student__in=students,
                                               student__house=house,
                                               session=session)
        context = {
            "reports": reports,
            "session": session,
            "remarks": Remark.objects.all(),
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        report_ids = request.POST.getlist("report_ids")
        remarks = request.POST.getlist("remarks")

        # Validating user input
        if len(report_ids) != len(remarks):
            messages.warning(
                request,
                "Invalid record. Please do not leave any records half filled.")
            return redirect(request.META.get("HTTP_REFERER"))

        # Check class teacher permissions
        has_house_master_permission = True
        if not SessionReport.objects.filter(id__in=report_ids).first(
        ).student.house.house_master.user == request.user:
            has_house_master_permission = False

        # Updating records
        for report_id, remark in zip(report_ids, remarks):
            report = get_object_or_404(SessionReport, id=report_id)

            # Check whether user has the permission to modify this record.
            if not (request.user.has_perm("dashboard.manage_other_report") or
                    has_house_master_permission):  # Administrative permission.
                messages.error(
                    request,
                    "You do not have permission to view or modify this subject record."
                )
                return redirect(request.META.get("HTTP_REFERER"))

            # Updating record
            report.house_master_remark_id = remark
            report.save()

        messages.success(request, "Record successfully updated.")
        return redirect(request.META.get("HTTP_REFERER"))
