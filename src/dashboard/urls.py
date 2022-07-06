from django.urls import path

from . import views

# yapf: disable

app_name = "dashboard"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('delete/<str:model_name>/<str:instance_id>', views.DeleteModelView.as_view(), name='delete_model'),

    # Students
    path('students/', views.StudentsView.as_view(), name='students'),
]