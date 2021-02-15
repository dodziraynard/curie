from django.urls import path
from django_pdfkit import PDFView
from . import views

app_name = "pdf_engine"

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:student_id>", views.student_transcript, name="student_transcript"),
]
