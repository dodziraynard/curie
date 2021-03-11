from django.urls import path
from . import api

app_name = "ajax"
urlpatterns = [
    path("student-teacher-count", api.get_student_teacher_count),
    path("students", api.ListStudentsAPI.as_view()),
    path("class-subjects", api.ListClassSubjectsAPI.as_view()),
    path("subjects", api.ListAllSubjectsAPI.as_view()),
    path("teachers", api.ListTeachersAPI.as_view()),
    path("classes", api.ListClassesAPI.as_view()),
    path("courses", api.ListCoursesAPI.as_view()),
    path("house-masters", api.LisHouseMastersAPI.as_view()),
    path("teachers-subjects", api.TeacherClassSubjectCombinationsAPI.as_view()),
]