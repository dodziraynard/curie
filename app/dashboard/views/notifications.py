from random import sample
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
import pandas as pd
from django.db.models import Q
from io import BytesIO
from django.utils import timezone
from django.contrib import messages
from accounts.models import User

from dashboard.models import Klass, Notification, Record, SessionReport, Staff, Student
from dashboard.tasks import send_notification, send_notifications_with_id_tag
from setup.models import School, SchoolSession


class NotificationIndexView(PermissionRequiredMixin, View):
    template_name = "dashboard/notifications/index.html"
    permission_required = [
        "dashboard.view_dashboard",
        "setup.manage_notifications",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        return render(request, self.template_name)


class NotificationHistoryView(PermissionRequiredMixin, View):
    template_name = "dashboard/notifications/notifications.html"
    permission_required = [
        "dashboard.view_dashboard",
        "setup.manage_notifications",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        notifications = Notification.objects.all()
        query = request.GET.get("query")
        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")
        status = request.GET.get("status")

        if query:
            notifications = notifications.filter(destination__icontains=query)
        if status:
            notifications = notifications.filter(status__icontains=status)
        if from_date:
            notifications = notifications.filter(created_at__gte=from_date)
        if to_date:
            notifications = notifications.filter(created_at__lte=to_date)

        context = {
            "notifications": notifications.order_by("-created_at")[:300],
            **{k: v
               for k, v in request.GET.items()}
        }
        return render(request, self.template_name, context)

    def post(self, request):
        notificaiont_id = request.POST.get("notification_id")
        notificaion = get_object_or_404(Notification, id=notificaiont_id)
        send_notification.delay(notificaion.id)
        messages.info(request, "Messages queued for delivery successfully.")
        return redirect(request.META.get("HTTP_REFERER"))


class ComposeSMS(PermissionRequiredMixin, View):
    template_name = "dashboard/notifications/compose_sms.html"
    permission_required = [
        "dashboard.view_dashboard",
        "setup.manage_notifications",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        return render(request, self.template_name)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        message = request.POST.get("message")
        recipients = request.POST.get("recipients", "").replace(
            "\r", "").replace("\n", "").replace(" ", "").split(",")
        recipient_file = request.FILES.get("recipient_file")

        phone_numbers = [phone for phone in recipients if len(phone)==10 and phone[0] == "0"] #yapf: disable
        if recipient_file:
            df = pd.read_excel(BytesIO(recipient_file.file.read()),
                               skiprows=1,
                               dtype=str)
            for _, row in df.iterrows():
                phone = row['PHONE']
                if phone and len(phone) == 10 and phone[0] == "0":
                    phone_numbers.append(phone)

        request.session['message'] = message
        request.session['phone_numbers'] = phone_numbers

        return redirect("dashboard:preview_sms")


class SendPINNotification(PermissionRequiredMixin, View):
    template_name = "dashboard/notifications/pin_notification.html"
    permission_required = [
        "dashboard.view_dashboard",
        "setup.manage_notifications",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        return render(request, self.template_name)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        included_ids = request.POST.get("included_ids", "").replace(
            "\r", "").replace("\n", "").replace(" ", "").split(",")
        excluded_ids = request.POST.get("excluded_ids", "").replace(
            "\r", "").replace("\n", "").replace(" ", "").split(",")
        all_staff = "on" in request.POST.get("all_staff", "")
        all_students = "on" in request.POST.get("all_students", "")
        reset_pin = "on" in request.POST.get("reset_pin", "")

        staff_ids = [
            staff.user.username
            for staff in Staff.objects.filter(has_left=False)
        ] if all_staff else []
        student_ids = [
            student.user.username
            for student in Student.objects.filter(completed=False)
        ] if all_students else []

        users = User.objects.filter(
            username__in=included_ids + staff_ids +
            student_ids).exclude(Q(phone=None) | Q(
                username__in=excluded_ids)).values("username")
        if not users:
            messages.error(request, "No users found.")
            return redirect("dashboard:send_pin_sms")

        request.session['usernames'] = [user.get("username") for user in users]
        request.session['reset_pin'] = reset_pin
        return redirect("dashboard:confirm_pin_notification")


class ConfirmPINNotification(PermissionRequiredMixin, View):
    template_name = "dashboard/notifications/confirm_pin_notification.html"
    permission_required = [
        "dashboard.view_dashboard",
        "setup.manage_notifications",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        usernames = request.session.get('usernames')
        if not usernames:
            messages.error(request, "No users found.")
            return redirect("dashboard:notifications")

        context = {
            "usernames": usernames,
        }
        return render(request, self.template_name, context=context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        usernames = request.session.get('usernames')
        reset_pin = request.session.get('reset_pin')

        if not usernames:
            messages.error(request, "No users found.")
            return redirect("dashboard:notifications")

        users = User.objects.filter(username__in=usernames)
        id_tag = timezone.now().strftime("%y%m%d%H%M%S%f")
        sender_id = School.objects.first().sms_sender_id
        for user in users:
            if not user.phone: continue

            if reset_pin or not user.temporal_pin:
                user.temporal_pin = "".join(
                    sample(list(map(str, [1, 2, 3, 4, 5, 6, 7, 8, 9, 0])), 4))
                user.set_password(user.temporal_pin)
                user.save()
            message = f"Dear {user.get_name()}, Your default PIN is {user.temporal_pin}."
            Notification.objects.create(text=message,
                                        id_tag=id_tag,
                                        status="new",
                                        purpose="PIN_RESET",
                                        sender_id=sender_id,
                                        destination=user.phone,
                                        initiated_by=request.user)
        send_notifications_with_id_tag.delay(id_tag)
        messages.info(request, "Messages queued for delivery successfully.")
        # Delete confirmation page details.
        request.session.pop('usernames')
        request.session.pop('reset_pin')
        return redirect("dashboard:notifications")


class PreviewSMS(PermissionRequiredMixin, View):
    template_name = "dashboard/notifications/preview_sms.html"
    permission_required = [
        "dashboard.view_dashboard",
        "setup.manage_notifications",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        message = request.session.get('message')
        phone_numbers = request.session.get('phone_numbers')
        if not (message and phone_numbers):
            messages.error(request, "No message or phone numbers found.")
            return redirect("dashboard:compose_sms")

        context = {
            "message": message,
            "phone_numbers": phone_numbers,
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        message = request.session.get('message')
        phone_numbers = request.session.get('phone_numbers')
        if not (message and phone_numbers):
            messages.error(request, "No message or phone numbers found.")
            return redirect("dashboard:compose_sms")

        id_tag = timezone.now().strftime("%y%m%d%H%M%S%f")
        sender_id = School.objects.first().sms_sender_id
        for phone in phone_numbers:
            Notification.objects.create(text=message,
                                        id_tag=id_tag,
                                        status="new",
                                        purpose="GENERAL",
                                        sender_id=sender_id,
                                        destination=phone,
                                        initiated_by=request.user)
        send_notifications_with_id_tag.delay(id_tag)
        messages.info(request, "Messages queued for delivery successfully.")

        # Delete preview messages and numbers from session cache
        request.session.pop('message')
        request.session.pop('phone_numbers')
        return redirect("dashboard:compose_sms")


class SendReportNotification(PermissionRequiredMixin, View):
    template_name = "dashboard/notifications/report_notifications.html"
    permission_required = [
        "dashboard.view_dashboard",
        "setup.manage_notifications",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        sessions = SchoolSession.objects.all()
        classes = Klass.objects.all()

        context = {
            "sessions": sessions,
            "classes": classes,
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        session_id = request.POST.get("session")
        classes = request.POST.getlist("classes")
        student_ids = request.POST.get("student_ids",
                                       "").replace(" ",
                                                   "").replace("\r",
                                                               "").split(",")
        session = get_object_or_404(SchoolSession, pk=session_id)
        records = Record.objects.filter(
            Q(session=session, klass_id__in=classes)
            | Q(session=session, student__student_id__in=student_ids))

        student_ids = list(
            set(records.values_list("student__student_id", flat=True)))

        session_reports = SessionReport.objects.filter(session=session)

        data = [
            (records.filter(student__student_id=student_id),
             session_reports.filter(student__student_id=student_id).first())
            for student_id in student_ids
        ]

        request.session['session_id'] = session_id
        request.session['classes'] = classes
        request.session['student_ids'] = student_ids
        request.session['data_size'] = len(data)
        return redirect("dashboard:report_notification_confirmation")


class ConfirmReportNotification(PermissionRequiredMixin, View):
    template_name = "dashboard/notifications/report_notification_confirmation.html"
    permission_required = [
        "dashboard.view_dashboard",
        "setup.manage_notifications",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        data_size = request.session.get('data_size')
        student_ids = request.session.get('student_ids')
        session_id = request.session.get('session_id')
        if not data_size:
            messages.error(request, "No results found.")
            return redirect("dashboard:report_notifications")

        context = {
            "data_size": data_size,
            "student_ids": student_ids,
            "session_id": session_id,
        }
        return render(request, self.template_name, context=context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        session_id = request.session.get('session_id')
        classes = request.session.get('classes')
        student_ids = request.session.get('student_ids')

        session = get_object_or_404(SchoolSession, pk=session_id)
        records = Record.objects.filter(
            Q(session=session, klass_id__in=classes)
            | Q(session=session, student__student_id__in=student_ids))

        student_ids = set(records.values_list("student__student_id",
                                              flat=True))
        session_reports = SessionReport.objects.filter(session=session)

        id_tag = timezone.now().strftime("%y%m%d%H%M%S%f")
        for student_id in student_ids:
            student_records = records.filter(student__student_id=student_id)
            session_report = session_reports.filter(
                student__student_id=student_id).first()
            message = f"STUDENT REPORT\nName: {session_report.student.user.get_name()}\nClass: {session_report.klass.name}"
            for record in student_records:
                message += f"\n{record.subject.name.title()} - {record.grade}"

            message += "\nFULL REPORT AT: " + request.META.get(
                "HTTP_ORIGIN") + reverse(
                    "pdf:bulk_report"
                ) + f"?session={session_id}&student_ids={student_id}"
            if session_report.student.sms_number:
                Notification.objects.create(
                    text=message,
                    id_tag=id_tag,
                    status="new",
                    purpose="REPORT",
                    destination=session_report.student.sms_number,
                    initiated_by=request.user)

        send_notifications_with_id_tag.delay(id_tag)
        messages.info(request, "Messages queued for delivery successfully.")

        # Delete preview data from session cache
        request.session.pop('session_id')
        request.session.pop('classes')
        request.session.pop('student_ids')
        return redirect("dashboard:notifications")