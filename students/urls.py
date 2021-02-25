from django.urls import path
from . import views

app_name = "students"
urlpatterns = [
    path("", views.students, name="students"),
    path("student-admission", views.student_admission, name="student_admission"),
    path("student-admission-sheet", views.student_admission_sheet,
         name="student_admission_sheet"),
    path("student-edit/<int:student_id>",
         views.edit_student, name="edit_student"),
    path("delete-student", views.delete_student, name="delete_student"),
    path("student-detail/<str:student_id>",
         views.student_detail, name="student_detail"),
]
