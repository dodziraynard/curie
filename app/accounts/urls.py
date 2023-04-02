from django.urls import path

from . import views

app_name = "accounts"

#yapf: disable
urlpatterns = [
    path('', views.ProfileView.as_view(), name='index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('users', views.UsersView.as_view(), name='users'),
    path('users/create-update', views.CreateUpdatUserView.as_view(), name="create_update_user"),
]
