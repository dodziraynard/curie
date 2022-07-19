from django.urls import path
from . import views

app_name = "pdf"

#yapf: disable
urlpatterns = [
    path('report-per-session/session/<str:session_id>/', views.AcademicRecordReportView.as_view(), name="report_per_session"),
]
