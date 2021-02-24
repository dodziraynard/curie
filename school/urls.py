from django.urls import path
from . import views

app_name = "school"
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("students", views.students, name="students"),
    path("student-admission", views.student_admission, name="student_admission"),
    path("student-admission-sheet", views.student_admission_sheet, name="student_admission_sheet"),
]
