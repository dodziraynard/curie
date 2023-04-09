import logging
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from dashboard.models import Student
from lms.utils.constants import (InvoiceItemType, InvoiceStatus,
                                 TransactionDirection, TransactionStatus,
                                 TransactionStatusMessages)
from setup.models import SchoolSession
from django.db import transaction as django_db_transaction
from django.utils.decorators import method_decorator

User = get_user_model()
logger = logging.getLogger("app")

#yapf: disable
# class Transaction(models.Model):
#     TRANSACTION_TYPE = [

#     ]
#     amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     deleted = models.BooleanField(default=False)
#     user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="transactions")


class Invoice(models.Model):
    INVOICE_STATUS = [
        (InvoiceStatus.APPLIED.value,InvoiceStatus.APPLIED.value),
        (InvoiceStatus.DRAFT.value,InvoiceStatus.DRAFT.value),
        (InvoiceStatus.PENDING.value,InvoiceStatus.PENDING.value),
    ]
    students = models.ManyToManyField(Student)
    name = models.TextField()
    due_date = models.DateTimeField(null=True, blank=True)
    note = models.TextField()
    status = models.CharField(max_length=100, choices=INVOICE_STATUS)
    session = models.ForeignKey(SchoolSession, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name="created_invoices", on_delete=models.PROTECT)
    updated_by = models.ForeignKey(User, related_name="updated_invoices", on_delete=models.PROTECT)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def model_name(self):
        return self.__class__.__name__.lower()

    @property
    def student_count(self):
        return self.students.all().count()

    @property
    def total_amount(self):
        amount = 0
        for item in self.invoice_items.all():
            amount += item.amount if item.type == InvoiceItemType.DEBIT.value else -item.amount
        return round(float(amount), 2)


class InvoiceItem(models.Model):
    INVOICE_ITEM_TYPES = [
        (InvoiceItemType.DEBIT.value, InvoiceItemType.DEBIT.value),
        (InvoiceItemType.CREDIT.value, InvoiceItemType.CREDIT.value),
    ]
    invoice = models.ForeignKey(Invoice, related_name="invoice_items", on_delete=models.CASCADE)
    name = models.TextField(max_length=200)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    type = models.CharField(max_length=100, choices=INVOICE_ITEM_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name="created_invoice_items", on_delete=models.PROTECT)
    updated_by = models.ForeignKey(User, related_name="updated_invoice_items", on_delete=models.PROTECT)

    def model_name(self):
        return self.__class__.__name__.lower()


class Transaction(models.Model):
    TRANSACTION_STATUS = [
        ("new", "New"),
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    ]
    TRANSACTION_DIRECTION = [
        (TransactionDirection.IN.value,TransactionDirection.IN.value),
        (TransactionDirection.OUT.value,TransactionDirection.OUT.value),
    ]
    def generate_id():
        return timezone.now().strftime("%y%m%d%H%M%S%f")

    transaction_id = models.CharField(max_length=20, unique=True, default=generate_id)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    account = models.ForeignKey("accounts.Account", on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    network = models.CharField(max_length=255, blank=True, null=True)
    fullname = models.CharField(max_length=255, blank=True, null=True)
    response_data = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    initiated_by = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True)
    direction = models.CharField(max_length=10, choices=TRANSACTION_DIRECTION)
    status = models.CharField(max_length=255, blank=True, null=True, choices=TRANSACTION_STATUS, default="new")
    status_message = models.CharField(max_length=255, blank=True, null=True)
    account_balances_updated = models.BooleanField(default=False)
    accepted_by_provider = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def success(self):
        return self.status == TransactionStatus.SUCCESS.value

    @method_decorator(django_db_transaction.atomic())
    def update_account_balances(self):
        if not self.account:
            logger.info(f"Transaction {self.transaction_id} does not have account.")
            return

        if not self.success():
            logger.info(f"Transaction {self.transaction_id} is not successful")
            return

        if self.account_balances_updated:
            logger.info(
                f"Transaction {self.transaction_id} account balances are already updated"
            )
            return

        if self.direction == TransactionDirection.IN.value:
            self.account.credit_account(self.amount)

        elif self.direction == TransactionDirection.OUT.value:
            self.account.credit_account(-self.amount)

        self.account_balances_updated = True
        self.paid = True
        self.save()
        return True