"""
This module is responsible for processing files using the celery worker
"""
import bisect
from dashboard.tasks import send_notification
from pdf_processor.utils import render_to_pdf_file
from django.conf import settings
from celery import shared_task
import logging
from collections import namedtuple
import django
from dashboard.models import Notification, Record, SessionReport, Student
from django.db.models import Q
from django.db.models import Sum

from graphql_api.models.accounting import Invoice
from setup.models import School, SchoolSession
from django.utils import timezone
from num2words import num2words

django.setup()


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
def generate_bulk_pdf_bill_sheet(self, invoice_id, filename="file.pdf", student_ids=None):
    set_task_state(self,
                   "RETRIEVING RECORDS",
                   1,
                   info=f"Retrieving invoice data.")

    invoice = Invoice.objects.filter(id=invoice_id, deleted=False).first()
    if not invoice:
        set_task_state(self, "NO RECORD FOUND", 3, info="Done")
        return False

    records = []
    data = []
    total = invoice.total_amount
    Statement = namedtuple("Statement", "name type amount")
    for item in invoice.invoice_items.filter(deleted=False):
        statement = Statement(item.name, item.type, item.amount)
        data.append(statement)

    students = invoice.students.filter(deleted=False).order_by("user__surname")
    if student_ids:
        students = students.filter(student_id__in=student_ids)
    for student in students:
        arears = round(total - float(student.user.account.amount_payable),
                       2)
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

    set_task_state(
        self,
        "WRITING",
        2,
        info=f"Found {len(records)} records. Writing the pdf ......")
    render_to_pdf_file("pdf_processor/bulk-student-bill-sheet.html", filename,
                       context)

    # Preparing link
    set_task_state(self, "GENERATING", 3, info="Generating download link")
    set_task_state(self, "DONE", 3, info="Done")


@shared_task(bind=True)
def generate_bulk_pdf_report(self,
                             session_id,
                             classes,
                             student_ids,
                             filename="file.pdf"):
    set_task_state(self,
                   "RETRIEVING RECORDS",
                   1,
                   info=f"Retrieving report data.")

    session = SchoolSession.objects.filter(
        deleted=False, pk=session_id).first()
    records = Record.objects.filter(deleted=False).filter(
        Q(session=session, klass_id__in=classes)
        | Q(session=session, student__student_id__in=student_ids)).exclude(total=None)

    student_ids = set(records.values_list("student__student_id", flat=True))

    session_reports = SessionReport.objects.filter(session=session)

    data = []

    for student_id in student_ids:
        student = Student.objects.filter(student_id=student_id).first()
        if not student:
            continue
        st_records = records.filter(
            student__student_id=student_id).distinct("subject__name").order_by("subject__name")
        st_reports = session_reports.filter(
            student__student_id=student_id).first()

        average_pos = "N/A"
        results = Record.objects.filter(klass=student.klass, deleted=False).exclude(total=None).values(
            'student__student_id').annotate(total_record=Sum('total')).order_by("-total_record")
        totals = sorted([-record["total_record"] for record in results])
        for result in results:
            if result.get("student__student_id") == student_id:
                pos = bisect.bisect_left(totals, -result.get("total_record")) + 1
                average_pos = num2words(pos, to="ordinal_num")
                break
        data.append((st_records, st_reports, average_pos))

    context = {
        "session": session,
        "school": School.objects.first(),
        "data": data,
        "current_time": timezone.now(),
    }

    # Writing PDF
    parent = settings.BASE_DIR / "assets/generated/"
    parent.mkdir(parents=True, exist_ok=True)
    filename = parent / filename

    set_task_state(self,
                   "WRITING",
                   2,
                   info=f"Found {len(data)} records. Writing the pdf ......")
    render_to_pdf_file("pdf_processor/bulk-student-report.html", filename,
                       context)

    # Preparing link
    set_task_state(self, "GENERATING", 3, info="Generating download link")
    set_task_state(self, "DONE", 3, info="Done")


@shared_task()
def generate_student_bill_sheet(session_id, student_ids=None):
    invoices = Invoice.objects.filter(session_id=session_id, deleted=False)
    urls = {}
    for invoice in invoices:
        data = []
        total = float(invoice.total_amount)
        Statement = namedtuple("Statement", "name type amount")
        for item in invoice.invoice_items.filter(deleted=False):
            statement = Statement(item.name, item.type, item.amount)
            data.append(statement)

        students = invoice.students.filter(
            deleted=False, student_id__in=student_ids).order_by("user__surname")
        for student in students:
            records = []
            arears = round(total - float(student.user.account.amount_payable),
                           2)
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
            invoice_name = "".join(
                c for c in invoice.name.lower().strip() if c.isalpha() or c == " ")
            filename = invoice_name + "-" + student.student_id.lower() + ".pdf"
            filename = filename.replace(" ", "-")
            files_dirs = "assets/generated/individual-bills/"
            parent = settings.BASE_DIR / files_dirs
            parent.mkdir(parents=True, exist_ok=True)
            filename_absolute = parent / filename
            render_to_pdf_file("pdf_processor/bulk-student-bill-sheet.html", filename_absolute,
                               context)
            urls[student.student_id] = files_dirs + filename
    return urls


@shared_task()
def generate_and_send_bill_via_sms(session_id, student_ids=None, base_url="http://127.0.0.1:8000/", initiation_user_id=1):
    urls = generate_student_bill_sheet(
        session_id=session_id, student_ids=student_ids)

    invoices = Invoice.objects.filter(session_id=session_id, deleted=False)
    for invoice in invoices:
        total = invoice.total_amount
        for student in invoice.students.filter(deleted=False, student_id__in=student_ids):
            sms_lines = [
                "Dear Parent,", f"Bill summary for your ward, {student.user.get_name()}, {invoice.session.name}:",
            ]
            arears = round(
                total - float(student.user.account.amount_payable), 2)
            arears = [0.00, arears][arears != 0]
            sms_lines.append(f"Arrears : GHC{arears}.")
            sms_lines.append(
                f"Amount payable: GHC{student.user.account.amount_payable}.")

            sms_lines.append(
                f"Full report: {base_url}{urls[student.student_id]}")
            sms_text = "\n".join(sms_lines)

            if student.sms_number:
                notification = Notification.objects.create(text=sms_text,
                                                           status="new",
                                                           purpose="BILL",
                                                           destination=student.sms_number,
                                                           initiated_by_id=initiation_user_id)
                send_notification(notification.id)
