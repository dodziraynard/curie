from django.urls import path
from . import views

app_name = "staff"
urlpatterns = [
    path("", views.staff, name="staff"),
    path("new-staff", views.new_staff, name="new_staff"),
    path("new-staff-sheet", views.new_staff_sheet, name="new_staff_sheet"),
    path("staff-edit/<str:staff_id>", views.edit_staff, name="edit_staff"),
    path("delete-staff", views.delete_staff, name="delete_staff"),
    path("staff-detail/<str:staff_id>", views.staff_detail, name="staff_detail"),
]
