"""
This module is responsible for processing files using the celery worker
"""
from collections import namedtuple
import django

from graphql_api.models.accounting import Invoice
from setup.models import School
from django.utils import timezone

django.setup()

import logging
from datetime import datetime

from celery import shared_task
from django.conf import settings

from pdf_processor.utils import render_to_pdf_file

logger = logging.getLogger("django")


def set_task_state(task,
                   message,
                   current,
                   total=3,
                   info="Processing",
                   link=None):
    try:
        task.update_state(state=message,
                          meta={
                              "current": str(current),
                              "total": total,
                              "info": info,
                              "link": link
                          })
    except Exception as e:
        logger.error(str(e))
        return


@shared_task(bind=True)
def generate_bulk_pdf_report(self, filename="file.pdf"):
    # Retrieving data
    # set_task_state(self,
    #                "RETRIEVING",
    #                1,
    #                info=f"Found {registrations.count()} records.")

    context = {
        "current_time": datetime.now().strftime("%d %B, %Y"),
    }

    # Writing PDF
    parent = settings.BASE_DIR / "assets/generated/"
    parent.mkdir(parents=True, exist_ok=True)
    filename = parent / filename

    set_task_state(self,
                   "WRITING",
                   2,
                   info=f"Writing the pdf: Found {4} records.")
    render_to_pdf_file('pdf_engine/general_report.html', filename, context)

    # Preparing link
    set_task_state(self, "GENERATING", 3, info="Generating download link")
    set_task_state(self, "DONE", 3, info="Done")


@shared_task(bind=True)
def generate_bulk_pdf_bill_sheet(self, invoice_id, filename="file.pdf"):
    set_task_state(self,
                   "RETRIEVING RECORDS",
                   1,
                   info=f"Retrieving invoice data.")

    invoice = Invoice.objects.filter(id=invoice_id).first()
    if not invoice:
        set_task_state(self, "NO RECORD FOUND", 3, info="Done")
        return

    records = []
    data = []
    total = invoice.total_amount
    Statement = namedtuple("Statement", "name type amount")
    for item in invoice.invoice_items.filter(deleted=False):
        statement = Statement(item.name, item.type, item.amount)
        data.append(statement)

    for student in invoice.students.all():
        arears = round(total - float(student.user.account.amount_payable),
                       2) * -1
        arears = [0.00, arears][arears != 0]
        records.append([student, total, arears, data[::]])

    context = {
        "session": invoice.session,
        "school": School.objects.first(),
        "records": records,
        "invoice": invoice,
        "current_time": timezone.now(),
    }

    # Writing PDF
    parent = settings.BASE_DIR / "assets/generated/"
    parent.mkdir(parents=True, exist_ok=True)
    filename = parent / filename

    set_task_state(self,
                   "WRITING",
                   2,
                   info=f"Writing the pdf: Found {4} records.")
    render_to_pdf_file("pdf_processor/bulk-student-bill-sheet.html", filename,
                       context)

    # Preparing link
    set_task_state(self, "GENERATING", 3, info="Generating download link")
    set_task_state(self, "DONE", 3, info="Done")
