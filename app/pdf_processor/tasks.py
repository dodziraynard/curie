"""
This module is responsible for processing files using the celery worker
"""
import django

django.setup()


import logging
import time
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
