from django.urls import path
from . import views

app_name = "pdf"

#yapf: disable
urlpatterns = [
    path('single-report/session/<str:session_id>/<str:class_id>/<str:student_id>', views.SingleAcademicRecordReportView.as_view(), name="single_report"),
    path('bulk-report/', views.BulkAcademicRecordReportView.as_view(), name="bulk_report"),

    path('student-full-report/<str:student_id>', views.StudentFullReportView.as_view(), name="student_full_report"),
]
