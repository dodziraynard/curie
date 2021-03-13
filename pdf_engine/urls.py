from django.urls import path
from django_pdfkit import PDFView
from . import views

app_name = "pdf_engine"

urlpatterns = [
    path("generate-student-reports/<str:student_id>", views.generate_semester_report, name="generate_semester_report"),
    path("generate-semester-reports", views.generate_semester_reports, name="generate_semester_reports"),
    
    # Url patterns for transcript
    path("semester-reports", views.semester_reports, name="semester_reports"),
]

