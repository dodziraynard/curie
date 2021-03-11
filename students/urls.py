from django.urls import path
from . import views

app_name = "students"
urlpatterns = [
     # Url patterns for students
     path("", views.students, name="students"),
     path("new-student", views.new_student, name="new_student"),
     path("new-student-sheet", views.new_student_sheet, name="new_student_sheet"),
     path("student-edit/<str:student_id>", views.edit_student, name="edit_student"),
     path("delete-student", views.delete_student, name="delete_student"),
     path("student-detail/<str:student_id>", views.student_detail, name="student_detail"),
     path("promotion", views.promotion, name="promotion"),

     # Url patterns for classes
     path("classes", views.classes, name="classes"),
     path("new-class", views.new_class, name="new_class"),
     path("class-edit/<str:class_id>", views.edit_class, name="edit_class"),
     path("delete-class", views.delete_class, name="delete_class"),
     path("class-detail/<str:class_id>", views.class_detail, name="class_detail"),

     # Url patterns for subjects
     path("subjects", views.subjects, name="subjects"),
     path("new-subject", views.new_subject, name="new_subject"),
     path("new-subject-sheet", views.new_subject_sheet, name="new_subject_sheet"),
     path("delete-subject", views.delete_subject, name="delete_subject"),
     path("subject-detail/<str:subject_id>", views.subject_detail, name="subject_detail"),
     path("subject-edit/<str:subject_id>", views.edit_subject, name="edit_subject"),

     # Url patterns for courses
     path("courses", views.courses, name="courses"),
     path("new-course", views.new_course, name="new_course"),
     path("new-course-sheet", views.new_course_sheet, name="new_course_sheet"),
     path("delete-course", views.delete_course, name="delete_course"),
     path("course-detail/<str:course_id>", views.course_detail, name="course_detail"),
     path("course-edit/<str:course_id>", views.edit_course, name="edit_course"),

     # Url patterns for house_masters
     path("house_masters", views.house_masters, name="house_masters"),
     path("new-house-master", views.new_house_master, name="new_house_master"),
     path("new-house_master-sheet", views.new_house_master_sheet, name="new_house_master_sheet"),
     path("delete-house-master", views.delete_house_master, name="delete_house_master"),
     path("house-master-detail/<str:house>", views.house_master_detail, name="house_master_detail"),
     path("house-master-edit/<str:house>", views.edit_house_master, name="edit_house_master"),
]
