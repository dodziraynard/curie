"""
This module is responsible for processing files using the celery worker
"""
from collections import defaultdict
from logging import Logger
from celery import shared_task
from django.urls import reverse
from django.db.models import Q
from dashboard.models import Klass, Notification, Record, Student, Subject, SubjectMapping, Task, StudentPromotionHistory
from graphql_api.models.accounting import Invoice, InvoiceItem, Transaction
from lms.utils.constants import (InvoiceItemType, InvoiceStatus, TaskStatus,
                                 TaskType, TransactionDirection)
from setup.models import School

logger = Logger("system")


@shared_task
def send_notifications_with_id_tag(id_tag):
    for notification in Notification.objects.filter(id_tag=id_tag):
        notification.send()


@shared_task
def send_notification(notification_id):
    notification = Notification.objects.filter(id=notification_id).first()
    if notification:
        notification.send()


@shared_task
def update_students_account(total_affected_student_ids, invoice_id):
    invoice = Invoice.objects.filter(id=invoice_id, deleted=False).first()
    if not invoice:
        return

    invoice.status = InvoiceStatus.PENDING.value
    invoice.save()
    students = Student.objects.filter(
        deleted=False, student_id__in=total_affected_student_ids)

    for student in students:
        total_in = 0
        total_out = 0
        transactions = Transaction.objects.filter(account=student.user.account,
                                                  deleted=False,
                                                  status="success")
        for transaction in transactions:
            if transaction.direction == TransactionDirection.IN.value:
                total_in += transaction.amount
            else:
                total_out += transaction.amount

        invoice_items = InvoiceItem.objects.filter(invoice__students=student,
                                                   deleted=False,
                                                   invoice__deleted=False)
        for item in invoice_items:
            if item.type.lower() == InvoiceItemType.CREDIT.value:
                total_in += item.amount
            elif item.type.lower() == InvoiceItemType.DEBIT.value:
                total_out += item.amount
        student.user.account.reset_balance(total_in - total_out)

    invoice.status = InvoiceStatus.APPLIED.value
    invoice.save()


@shared_task
def create_or_update_user_academic_record_tasks():
    current_session = School.objects.first().current_session
    mappings = SubjectMapping.objects.filter(session=current_session)

    students = Student.objects.filter(deleted=False, completed=False)
    class_subject_pending_count = defaultdict(int)
    for student in students:
        klass = StudentPromotionHistory.get_class(student, current_session)
        subjects = student.get_subjects()
        for subject in subjects:
            valid_record_exists = Record.objects.exclude(Q(class_score=None) | Q(exam_score=None))\
                .filter(deleted=False,
                        klass=klass,
                        student=student, subject=subject, session=current_session).exists()
            key = "|".join([klass.class_id, subject.code])
            class_subject_pending_count[key] += not valid_record_exists

    for key, pending_count in class_subject_pending_count.items():
        class_class_id, subject_code = key.split("|")
        klass = Klass.objects.filter(class_id=class_class_id,
                                     deleted=False).first()
        subject = Subject.objects.filter(code=subject_code,
                                         deleted=False).first()
        mapping = mappings.filter(subject=subject, klass=klass).first()
        if not mapping:
            logger.info(f"No mapping for {mapping}")
            continue

        task_code = key
        redirect_link = reverse("dashboard:academic_record_data") + \
            f"?session={current_session.id}&subject={subject.id}&classes={klass.id}"
        user = mapping.staff.user if mapping.staff else None
        task, created = Task.objects.get_or_create(
            assigned_to=user,
            session=current_session,
            deleted=False,
            task_code=task_code,
            task_type=TaskType.ACADEMIC_RECORD.value,
        )
        if pending_count > 0:
            message = f"You have {pending_count} records pending upload for {subject.name} in {klass.name}."
            task.status = TaskStatus.PENDING.value
            task.redirect_link = redirect_link
        else:
            message = f"You have successfully uploaded all records for {subject.name} in {klass.name}."
            task.status = TaskStatus.COMPLETED.value
        task.expires_at = current_session.end_date
        task.message = message
        task.save()
