from django.db import models
from students.models import Klass, Subject
from django.utils import timezone
from django.contrib.auth.models import User
from . utils import time_left as tl


class Notification(models.Model):
    message = models.TextField()
    time_stamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.message


class PromotionHistory(models.Model):
    old_class = models.ForeignKey(
        Klass, related_name="old_history",  on_delete=models.CASCADE)
    new_class = models.ForeignKey(
        Klass, related_name="new_history", on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Promotion Histories"


class School(models.Model):
    name = models.CharField(max_length=500)
    code = models.CharField(max_length=50)
    sender_id = models.CharField(
        verbose_name="SMS Sender ID", max_length=11, null=True, blank=True)
    sms_api_key = models.CharField(max_length=200, null=True, blank=True)
    crest = models.FileField(upload_to="uploads/images",
                             default="/assets/images/crest.png")
    current_semester = models.IntegerField(default="1")
    current_academic_year = models.CharField(max_length=20, default="2020/2021")

    def __str__(self):
        return self.name


class UploadedFile(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="uploads")
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class SubjectTeacherTask(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="uploads/records")
    academic_year = models.CharField(max_length=100)
    semester = models.CharField(max_length=50)
    klass = models.ForeignKey(Klass, on_delete=models.CASCADE)
    subject = models.ForeignKey(
        Subject, null=True, blank=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(default=timezone.now)
    deadline = models.DateTimeField(null=True)
    message = models.TextField(null=True, blank=True)
    replied = models.OneToOneField(
        UploadedFile, related_name="subject_teacher_task", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = "{} - {} {}".format(self.subject.name,
                                        self.semester, self.academic_year)
        super(SubjectTeacherTask, self).save(*args, **kwargs)

    def time_left(self):
        return tl(self.deadline)


class ClassTeacherTask(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="uploads/house master")
    academic_year = models.CharField(max_length=100)
    semester = models.CharField(max_length=50)
    klass = models.ForeignKey(Klass, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    deadline = models.DateTimeField(null=True)
    replied = models.OneToOneField(
        "UploadedFile", related_name="class_teacher_request", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = "{} - {} {} Remarks".format(
            self.academic_year, self.semester, self.student_class.name)
        super(ClassTeacherTask, self).save(*args, **kwargs)

    def time_left(self):
        return tl(self.deadline)


class HouseMasterTask(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="uploads/house master")
    academic_year = models.CharField(max_length=100)
    semester = models.CharField(max_length=50)
    klass = models.ForeignKey(Klass, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    deadline = models.DateTimeField(null=True)
    replied = models.OneToOneField(
        UploadedFile, related_name="house_master_task", null=True, blank=True, on_delete=models.SET_NULL)
    house = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = "{} - {} {} Remarks".format(
            self.academic_year, self.semester, self.klass.name)
        super(HouseMasterTask, self).save(*args, **kwargs)

    def time_left(self):
        return tl(self.deadline)
