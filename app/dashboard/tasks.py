"""
This module is responsible for processing files using the celery worker
"""
from celery import shared_task

from dashboard.models import Notification, Student
from graphql_api.models.accounting import Invoice, InvoiceItem, Transaction
from lms.utils.constants import InvoiceItemType, InvoiceStatus, TransactionDirection


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
    invoice = Invoice.objects.filter(id=invoice_id).first()
    if not invoice: return

    invoice.status = InvoiceStatus.PENDING.value
    invoice.save()
    students = Student.objects.filter(
        student_id__in=total_affected_student_ids)

    for student in students:
        total_in = 0
        total_out = 0
        transactions = Transaction.objects.filter(account=student.user.account,
                                                  status="success")
        for transaction in transactions:
            if transaction.direction == TransactionDirection.IN.value:
                total_in += transaction.amount
            else:
                total_out += transaction.amount

        invoice_items = InvoiceItem.objects.filter(invoice__students=student)
        for item in invoice_items:
            if item.type.lower() == InvoiceItemType.CREDIT.value:
                total_in += item.amount
            elif item.type.lower() == InvoiceItemType.DEBIT.value:
                total_out += item.amount
        student.user.account.reset_balance(total_in - total_out)

    invoice.status = InvoiceStatus.APPLIED.value
    invoice.save()
