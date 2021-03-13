from django.urls import path
from . import views

app_name = "sms"
urlpatterns = [
    path("messages", views.Messages.as_view(), name="messages"),
    path("new-sms", views.NewSMS.as_view(), name="new_sms"),
    path("forward-credentials", views.ForwardCredentials.as_view(), name="forward_credentials"),
    path("sms-balance", views.Balance.as_view(), name="balance"),

    path("resend-sms", views.ResendSMS.as_view(), name="resend-sms"),

]
