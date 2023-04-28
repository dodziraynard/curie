from django.urls import include, path
from . import views

app_name = "website"
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('about', views.AboutView.as_view(), name="about"),
    path('contact', views.ContactView.as_view(), name="contact"),
    path('enrollment', views.EnrollmentView.as_view(), name="enrollment"),
]
