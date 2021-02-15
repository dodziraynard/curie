from django.contrib import admin
from . models import (Student,
                      ClassTeacherRemark,
                      HouseMasterRemark,
                      Klass,
                      Course,
                      Subject,
                      Record,
                      TeacherClassSubjectCombination,
                      GradingSystem)

admin.site.register(Student)
admin.site.register(ClassTeacherRemark)
admin.site.register(HouseMasterRemark)
admin.site.register(Klass)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Record)
admin.site.register(TeacherClassSubjectCombination)
admin.site.register(GradingSystem)
