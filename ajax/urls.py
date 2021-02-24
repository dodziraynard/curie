from django.urls import path
from . import api

app_name = "ajax"
urlpatterns = [
    path("student-teacher-count", api.get_student_teacher_count),
    path("students", api.ListStudentsAPI.as_view()),
]
