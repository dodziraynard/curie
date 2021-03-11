from django.db import models
from staff.models import Staff
from django.contrib.auth.models import User
from django.conf import settings
from random import sample
from django.utils import timezone
import time


class Student(models.Model):
    student_id = models.CharField(max_length=100, unique=True)
    surname = models.CharField(max_length=100)
    other_names = models.CharField(max_length=100)
    sms_number = models.CharField(max_length=10)
    klass = models.ForeignKey("Klass", related_name="students",
                              on_delete=models.SET_NULL, null=True)
    electives = models.ManyToManyField(
        "Subject", related_name="students", blank=True)
    temporal_pin = models.CharField(max_length=10, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    activated = models.BooleanField(default=False)
    house = models.CharField(max_length=50)
    bio = models.TextField(null=True, blank=True)
    track = models.CharField(max_length=50)
    father = models.CharField(max_length=200, null=True, blank=True)
    mother = models.CharField(max_length=200, null=True, blank=True)
    completed = models.BooleanField(default=False)
    user = models.OneToOneField(
        User, related_name="student", on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(default=timezone.now)
    last_promotion_date = models.DateField(default=timezone.now)
    image = models.FileField(
        upload_to="media/images/students", default="/images/avatar.jpg")

    def my_class(self):
        return self.klass.name
    
    def promote(self):
        final_form = Klass.objects.order_by("-form").first().form
        self.last_promotion_date = timezone.now()
        if self.klass.form >= final_form:
            self.completed = True
        else:
            next_form = self.klass.form + 1
            next_class = Klass.objects.get(form=next_form, stream=self.klass.stream, course=self.klass.course)
            self.klass = next_class
        self.save()

    class Meta:
        db_table = "students"

    def __str__(self):
        return f"{self.surname} {self.other_names}"

    def get_full_name(self):
        return f"{self.surname} {self.other_names}"


class ClassTeacherRemark(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    semester = models.CharField(max_length=50)
    academic_year = models.CharField(max_length=50)
    klass = models.ForeignKey("klass", on_delete=models.CASCADE)
    attendance = models.IntegerField(default=0)
    total_attendance = models.IntegerField(default=0)
    attitude = models.CharField(max_length=100)
    interest = models.CharField(max_length=100)
    conduct = models.CharField(max_length=100)
    remark = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)

    class Meta:
        db_table = "class_teacher_remarks"

    def __str__(self):
        return f"{self.student.surname} - {self.semester} {self.academic_year}"


class HouseMasterRemark(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    semester = models.CharField(max_length=50)
    academic_year = models.CharField(max_length=50)
    remark = models.CharField(max_length=200)
    date = models.DateField(default=timezone.now)
    klass = models.ForeignKey(
        "klass", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "house_master_remarks"

    def __str__(self):
        return f"{self.student.surname} - {self.semester} {self.academic_year}"


class Klass(models.Model):
    class_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50, unique=True)
    class_teacher = models.OneToOneField(Staff, related_name="klass", null=True, on_delete=models.SET_NULL)
    form = models.IntegerField(default=1)
    stream = models.CharField(max_length=5)
    course = models.ForeignKey(
        "Course", related_name="classes", on_delete=models.CASCADE)

    @property
    def course_name(self):
        return self.course.name
    
    @property
    def class_teacher_name(self):
        return self.class_teacher.get_full_name() or "None"
    
    def get_student_count(self):
        return Student.objects.filter(completed=False, klass=self).count()

    class Meta:
        db_table = "classes"
        verbose_name_plural = "Classes"
        verbose_name = "Class"

    def __str__(self):
        return self.name

    def get_number_of_students(self):
        return self.students.all().count()


class Course(models.Model):
    course_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, unique=True)
    subjects = models.ManyToManyField("Subject", related_name="courses")

    class Meta:
        db_table = "courses"

    def __str__(self):
        return self.name

    @property
    def get_number_of_students(self):
        num = 0
        for klass in self.classes.all():
            num += klass.get_student_count()
        return num


class Subject(models.Model):
    subject_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, unique=True)
    is_elective = models.BooleanField()

    class Meta:
        db_table = "subjects"

    @property
    def student_count(self):
        if self.is_elective:
            return Student.objects.filter(completed=False, electives=self).count()
        return Student.objects.filter(completed=False).count()

    def __str__(self):
        return self.name

    def get_number_of_students(self):
        return self.students.all().count()


class Record(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    exam_score = models.IntegerField(default=0, blank=True, null=True)
    class_score = models.IntegerField(default=0, blank=True, null=True)
    total = models.IntegerField(default=0, blank=True, null=True)
    subject = models.ForeignKey("Subject", on_delete=models.PROTECT)
    klass = models.ForeignKey("Klass", on_delete=models.SET_NULL, null=True)
    grade = models.CharField(max_length=5, blank=True, null=True)
    remark = models.CharField(max_length=20, blank=True, null=True)
    position = models.CharField(max_length=5, blank=True, null=True)
    semester = models.CharField(max_length=50, blank=True, null=True)
    academic_year = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateField(default=timezone.now)
    roll_no = models.IntegerField(blank=True, null=True)
    rank = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = "academic_records"

    def __str__(self):
        return self.student.get_full_name()

    def save(self, *args, **kwargs):
        self.rank = f"{self.position}/{self.roll_no}"
        self.total = round(0.3 * float(self.class_score) +
                           0.7 * float(self.exam_score))

        grading_system = GradingSystem.objects.filter(
            min_score__lte=self.total).order_by("-min_score").first()
        if grading_system:
            self.grade = grading_system.grade
            self.remark = grading_system.remark
        else:
            self.grade = "F"
            self.remark = "Fail"

        super(Record, self).save(*args, **kwargs)


# Subject and the class a staff teaches
class TeacherClassSubjectCombination(models.Model):
    subject = models.ForeignKey(
        "Subject", on_delete=models.CASCADE, related_name="teachers")
    klass = models.ForeignKey(
        "Klass", verbose_name="Class", related_name="combinations", on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, related_name="teaches",
                              verbose_name="Staff", on_delete=models.CASCADE)
    
    class Meta:
        db_table = "teacher_class_subject_combination"

    def subject_name(self):
        return self.subject.name

    def class_name(self):
        return self.klass.name
    
    def teacher(self):
        return self.staff.get_full_name()


    def __str__(self):
        if self.subject and self.staff:
            return "{} - {}: {}".format(self.subject.name.capitalize(), self.klass.name, self.staff.surname)
        else:
            return str(self.id)


class GradingSystem(models.Model):
    min_score = models.IntegerField()
    grade = models.CharField(max_length=5)
    remark = models.CharField(max_length=50)

    class Meta:
        db_table = "grading_systems"

    def __str__(self):
        return f"{self.min_score} - {self.grade} - {self.remark}"
