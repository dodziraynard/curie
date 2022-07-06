from django.urls import path

from . import views

app_name = "setup"
urlpatterns = [
    path('', views.IndexView.as_view(), name="setup_index"),
    path('roles/<int:role_id>/', views.RoleManagementView.as_view(), name='roles_management')
]
