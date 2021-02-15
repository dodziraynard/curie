from django.contrib import admin
from . models import (Notification,
                      PromotionHistory,
                      School,
                      UploadedFile,
                      SubjectTeacherTask,
                      ClassTeacherTask,
                      HouseMasterTask)

admin.site.register(Notification)
admin.site.register(PromotionHistory)
admin.site.register(School)
admin.site.register(UploadedFile)
admin.site.register(SubjectTeacherTask)
admin.site.register(ClassTeacherTask)
admin.site.register(HouseMasterTask)
