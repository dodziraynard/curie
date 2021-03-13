from django.db import models
from django.utils import timezone
from . constants import SMS_FAILED, SMS_SENT, SMS_PENDING


class SMS(models.Model):
    STATUS = (
        (SMS_SENT,'Sent'),
        (SMS_FAILED,'Failed'),
        (SMS_PENDING,'Pending')
    )
    number = models.CharField(max_length=10)
    message = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, default=SMS_PENDING, choices=STATUS)
    res_code = models.CharField(max_length=10, null=True, blank=True)
    res_message = models.CharField(max_length=200, null=True, blank=True)
    
    def f_date(self):
        return self.date.strftime("%Y-%m-%d %I:%M:%S %p")
    def __str__(self):
        return f"{self.number} "+ self.message[:100]
