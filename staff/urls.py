from django.urls import path
from . import views

app_name = "staff"
urlpatterns = [
    path("", views.staff, name="staff"),
    path("staff-admission", views.staff_admission, name="staff_admission"),
    path("staff-admission-sheet", views.staff_admission_sheet,
         name="staff_admission_sheet"),
    path("staff-edit/<str:staff_id>", views.edit_staff, name="edit_staff"),
    path("delete-staff", views.delete_staff, name="delete_staff"),
    path("staff-detail/<str:staff_id>", views.staff_detail, name="staff_detail"),
]
