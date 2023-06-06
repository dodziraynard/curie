from django.urls import path

from . import views

app_name = "pdf"

#yapf: disable
urlpatterns = [
    path('single-report/session/<str:session_id>/<str:student_id>', views.SingleAcademicRecordReportView.as_view(), name="single_report"),
    path('bulk-report/', views.BulkAcademicRecordReportView.as_view(), name="bulk_report"),

    path('personal-academic-report', views.PersonalAcadmicReport.as_view(), name="personal_academic_report"),
    # path('student-bill-sheet/<str:invoice_id>', views.BulkStudentBillSheet.as_view(), name="student_bill_sheet"),

    path('pesonal-transcript', views.PersonalTranscriptionView.as_view(), name="pesonal_transcript"),

]
