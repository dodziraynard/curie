from django.contrib import admin

from .models import Notification, Student, StudentPromotionHistory

# Register your models here.
admin.site.register(Student)
admin.site.register(Notification)
admin.site.register(StudentPromotionHistory)
