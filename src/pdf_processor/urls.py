from django.urls import path
from django_pdfkit import PDFView
from . import views

app_name = "pdf"

#yapf: disable
urlpatterns = [
    path('report-per-session', views.AcademicRecordReportView.as_view(), name="report_per_session"),
]
