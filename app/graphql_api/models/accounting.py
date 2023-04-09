from django.db import models
from dashboard.models import Student
from django.contrib.auth import get_user_model

from lms.utils.constants import InvoiceItemType, InvoiceStatus

User = get_user_model()

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
        (InvoiceStatus.PAID.value,InvoiceStatus.PAID.value),
        (InvoiceStatus.DRAFT.value,InvoiceStatus.DRAFT.value),
        (InvoiceStatus.PENDING.value,InvoiceStatus.PENDING.value),
    ]
    students = models.ManyToManyField(Student)
    name = models.TextField()
    due_date = models.DateTimeField(null=True, blank=True)
    note = models.TextField()
    status = models.CharField(max_length=100, choices=INVOICE_STATUS)

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
            amount += item.amount
        return round(amount, 2)


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