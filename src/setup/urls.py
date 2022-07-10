from django.urls import path

from . import views

app_name = "setup"

#yapf: disable
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path("role/change", views.CreateUpdateGroup.as_view(), name="change_role"),
    path('roles/<int:role_id>/', views.RoleManagementView.as_view(), name='roles_management'),


    path('create-update-attitude/', views.CreateUpdateAttitudeView.as_view(), name='create_update_attitude'),
    path('create-update-interest/', views.CreateUpdateInterestView.as_view(), name='create_update_interest'),
    path('create-update-conduct/', views.CreateUpdateConductView.as_view(), name='create_update_conduct'),
    path('create-update-track/', views.CreateUpdateTrackView.as_view(), name='create_update_track'),
    path('create-update-grading-system/', views.CreateUpdateGradingSystemView.as_view(), name='create_update_grading_system'),
    path('create-update-school-session/', views.CreateUpdateSchoolSessionView.as_view(), name='create_update_school_session'),
]
