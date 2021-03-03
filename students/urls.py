from django.urls import path
from . import views

app_name = "students"
urlpatterns = [
     path("", views.students, name="students"),
     path("new-student", views.new_student, name="new_student"),
     path("new-student-sheet", views.new_student_sheet, name="new_student_sheet"),
     path("student-edit/<str:student_id>", views.edit_student, name="edit_student"),
     path("delete-student", views.delete_student, name="delete_student"),
     path("student-detail/<str:student_id>", views.student_detail, name="student_detail"),

     path("classes", views.classes, name="classes"),
     path("new-class", views.new_class, name="new_class"),
     path("class-edit/<str:class_id>", views.edit_class, name="edit_class"),
     path("delete-class", views.delete_class, name="delete_class"),
     path("class-detail/<str:class_id>", views.class_detail, name="class_detail"),


     path("subjects", views.subjects, name="subjects"),
     path("new-subject", views.new_subject, name="new_subject"),
     path("new-subject-sheet", views.new_subject_sheet, name="new_subject_sheet"),
     path("delete-subject", views.delete_subject, name="delete_subject"),
     path("subject-detail/<str:subject_id>", views.subject_detail, name="subject_detail"),
     path("subject-edit/<str:subject_id>", views.edit_subject, name="edit_subject"),
]
