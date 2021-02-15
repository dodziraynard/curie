from random import sample
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


class Staff(models.Model):
    staff_id = models.CharField(max_length=100, unique=True)
    surname = models.CharField(max_length=100)
    other_names = models.CharField(max_length=100)
    sms_number = models.CharField(max_length=10)
    has_left = models.BooleanField(default=False)
    gender = models.CharField(max_length=10)
    has_class = models.BooleanField(default=True)
    temporal_pin = models.CharField(max_length=10)
    user = models.OneToOneField(
        User, related_name="staff", on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    activated = models.BooleanField(default=False)
    image = models.FileField(upload_to="uploads/images/staff",
                             default="assets/images/avatar.png")

    class Meta:
        db_table = "staff"
        verbose_name_plural = "Staff"

    def __str__(self):
        return self.surname

    # def get_number_of_students(self):
    #     number = 0

    #     # TODO: Try except
    #     for teach in self.teaches:
    #         number += teach.subject.students.all().count()
    #     return number


class HouseMaster(models.Model):
    staff = models.OneToOneField(
        "Staff", related_name="housemaster", on_delete=models.CASCADE)
    house = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        self.house = self.house.title()
        super(HouseMaster, self).save(*args, **kwargs)

    def __str__(self):
        return "{} {} - {}".format(self.staff.other_names, self.staff.surname, self.house)
