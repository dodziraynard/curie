from io import BytesIO
from random import sample

import pandas as pd
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.core.exceptions import PermissionDenied

from accounts.models import User
from dashboard.models import (Klass, Notification, Record, SessionReport,
                              Staff, Student)
from dashboard.tasks import send_notification, send_notifications_with_id_tag
from graphql_api.models.accounting import Invoice
from lms.utils.constants import (InvoiceItemType)
from pdf_processor.tasks import generate_and_send_bill_via_sms
from setup.models import School, SchoolSession


class NotificationIndexView(PermissionRequiredMixin, View):
    template_name = "dashboard/notifications/index.html"
    permission_required = [
        "setup.view_dashboard",
        "setup.view_alert",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        return render(request, self.template_name)


class NotificationHistoryView(PermissionRequiredMixin, View):
    template_name = "dashboard/notifications/notifications.html"
    permission_required = [
        "setup.view_dashboard",
        "setup.view_notification_history",
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
        if not request.user.has_perm("setup.resend_notification"):
            raise PermissionDenied()

        notificaiont_id = request.POST.get("notification_id")
        notificaion = get_object_or_404(Notification, id=notificaiont_id)
        send_notification.delay(notificaion.id)
        messages.info(request, "Messages queued for delivery successfully.")
        return redirect(request.META.get("HTTP_REFERER"))


class ComposeSMS(PermissionRequiredMixin, View):
    template_name = "dashboard/notifications/compose_sms.html"
    permission_required = [
        "setup.view_dashboard",
        "setup.compose_sms",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        return render(request, self.template_name)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        message = request.POST.get("message")
        all_students = "on" in request.POST.get("all_students", "")
        all_staff = "on" in request.POST.get("all_staff", "")

        recipients = request.POST.get("recipients", "").replace(
            "\r", "").replace("\n", "").replace(" ", "").split(",")
        recipient_file = request.FILES.get("recipient_file")

        phone_numbers = [phone for phone in recipients if len(
            phone) == 10 and phone[0] == "0"]  # yapf: disable
        if recipient_file:
            df = pd.read_excel(BytesIO(recipient_file.file.read()),
                               skiprows=1,
                               dtype=str)
            for _, row in df.iterrows():
                phone = row['PHONE']
                if phone and len(phone) == 10 and phone[0] == "0":
                    phone_numbers.append(phone)

        if all_students:
            students = Student.objects.filter(completed=False, deleted=False)
            student_phones = [
                student.sms_number for student in students if student.sms_number and student.sms_number[0] == "0"]  # yapf: disable
            phone_numbers.extend(student_phones)

        if all_staff:
            teachers = Staff.objects.filter(has_left=False, deleted=False)
            teacher_phones = [
                teacher.user.phone for teacher in teachers if teacher.user.phone and teacher.user.phone[0] == "0"]  # yapf: disable
            phone_numbers.extend(teacher_phones)

        request.session['message'] = message
        request.session['phone_numbers'] = list(set(phone_numbers))

        return redirect("dashboard:preview_sms")


class SendPINNotification(PermissionRequiredMixin, View):
    template_name = "dashboard/notifications/pin_notification.html"
    permission_required = [
        "setup.view_dashboard",
        "setup.send_pin_notification",
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
        "setup.view_dashboard",
        "setup.send_pin_notification",
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
            if not user.phone:
                continue

            if reset_pin or not user.temporal_pin:
                user.temporal_pin = "".join(
                    sample(list(map(str, [1, 2, 3, 4, 5, 6, 7, 8, 9, 0])), 4))
                user.set_password(user.temporal_pin)
                user.save()
            message = f"Dear {user.get_name()}, Your login credentials are:\nUsername: {user.username}\nDefualt PIN: {user.temporal_pin}."
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
        "setup.view_dashboard",
        "setup.compose_sms",
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
        "setup.view_dashboard",
        "setup.send_report_notification",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        sessions = SchoolSession.objects.filter(deleted=False)
        classes = Klass.objects.filter(deleted=False)

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
        "setup.view_dashboard",
        "setup.send_report_notification",
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
        id_tag = timezone.now().strftime("%y%m%d%H%M%S%f")
        for student_id in student_ids:
            student = Student.objects.filter(student_id=student_id)
            student_records = records.filter(student=student)

            message = f"STUDENT REPORT\nName: {student.user.get_name()}\nClass: {student_records.first().klass.name}"
            for record in student_records:
                message += f"\n{record.subject.name.title()} - {record.grade}"

            message += "\nFULL REPORT AT: " + request.META.get(
                "HTTP_ORIGIN") + reverse(
                    "pdf:bulk_report"
            ) + f"?session={session_id}&student_ids={student_id}"
            if student.sms_number:
                Notification.objects.create(text=message,
                                            id_tag=id_tag,
                                            status="new",
                                            purpose="REPORT",
                                            destination=student.sms_number,
                                            initiated_by=request.user)

        send_notifications_with_id_tag.delay(id_tag)
        messages.info(request, "Messages queued for delivery successfully.")

        # Delete preview data from session cache
        request.session.pop('session_id')
        request.session.pop('classes')
        request.session.pop('student_ids')
        return redirect("dashboard:notifications")


class SendBillNotification(PermissionRequiredMixin, View):
    template_name = "dashboard/notifications/bill_notifications.html"
    permission_required = [
        "setup.view_dashboard",
        "setup.send_bill_notification",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        sessions = SchoolSession.objects.filter(deleted=False)
        classes = Klass.objects.filter(deleted=False)

        context = {
            "sessions": sessions,
            "classes": classes,
        }
        return render(request, self.template_name, context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        session_id = request.POST.get("session")
        class_ids = request.POST.getlist("classes")
        student_ids = request.POST.get("student_ids",
                                       "").replace(" ",
                                                   "").replace("\r",
                                                               "").split(",")
        session = get_object_or_404(SchoolSession, pk=session_id)
        students = Student.objects.filter(
            completed=False, deleted=False, klass_id__in=class_ids)
        including_students = Student.objects.filter(
            student_id__in=student_ids, deleted=False)

        students = students.union(including_students)
        student_ids = students.values_list("student_id", flat=True)
        sample_invoice = Invoice.objects.filter(
            session=session, students__student_id__in=student_ids).first()
        request.session['session_id'] = session_id
        request.session['student_ids'] = list(set(student_ids))
        request.session['sample_invoice_id'] = sample_invoice.id if sample_invoice else None

        return redirect("dashboard:bill_notification_confirmation")


class ConfirmBillNotification(PermissionRequiredMixin, View):
    template_name = "dashboard/notifications/bill_notification_confirmation.html"
    permission_required = [
        "setup.view_dashboard",
        "setup.send_bill_notification",
    ]

    @method_decorator(login_required(login_url="accounts:login"))
    def get(self, request):
        sample_invoice_id = request.session.get('sample_invoice_id')
        student_ids = request.session.get('student_ids')
        session_id = request.session.get('session_id')
        if not sample_invoice_id:
            messages.error(request, "No results found.")
            return redirect("dashboard:bill_notifications")

        sample_invoice = Invoice.objects.filter(id=sample_invoice_id).first()
        sms_lines = [
            "Dear Parent,", f"Bill summary for your ward, {sample_invoice.students.first().user.get_name()}, {sample_invoice.session.name}:"]
        total = 0
        for item in sample_invoice.invoice_items.filter(deleted=False):
            sms_lines.append(f"{item.name} : GHS{item.amount} ({item.type}).")
            if item.type == InvoiceItemType.DEBIT.value:
                total += item.amount
            else:
                total -= item.amount
        sms_lines.append(f"Amount payable: GHS{total}.")
        sms_lines.append(
            f"Full report: {request.build_absolute_uri(reverse('dashboard:notifications'))}")
        sample_sms = "\n".join(sms_lines)
        context = {
            "sample_invoice": sample_invoice,
            "student_ids": student_ids,
            "session_id": session_id,
            "sample_sms": sample_sms,
        }
        return render(request, self.template_name, context=context)

    @method_decorator(login_required(login_url="accounts:login"))
    def post(self, request):
        student_ids = request.session.get('student_ids')
        session_id = request.session.get('session_id')

        generate_and_send_bill_via_sms.delay(
            session_id=session_id, student_ids=student_ids, base_url=request.build_absolute_uri(
                "/"),
            initiation_user_id=request.user.id
        )

        messages.info(request, "Task submitted successfully.")

        # Delete preview data from session cache
        request.session.pop('sample_invoice_id')
        request.session.pop('student_ids')
        request.session.pop('session_id')
        return redirect("dashboard:notifications")
