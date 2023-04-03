from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone
from lms.utils.functions import get_current_session

from setup.models import (Attitude, Conduct, GradingSystem, Interest,
                          ModelMixin, Remark, SchoolSession, Track)
from django.contrib.auth import get_user_model
from django.conf import settings
import requests

User = get_user_model()


# yapf: disable
class Relative(ModelMixin):
    RELATIONSHIP_STATUS = [
        ("mother", "mother"),
        ("father", "father"),
        ("guardian", "guardian"),
    ]
    fullname = models.CharField(max_length=200, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    education = models.CharField(max_length=100, null=True, blank=True)
    religion = models.CharField(max_length=100, null=True, blank=True)
    spouses = models.IntegerField(null=True, blank=True)
    date_of_demise = models.DateField(null=True, blank=True)
    relationship = models.CharField(max_length=100, choices=RELATIONSHIP_STATUS)
    user = models.OneToOneField(User,related_name="relative",on_delete=models.SET_NULL, null=True, blank=True)


#yapf: disable
class Student(ModelMixin):
    student_id = models.CharField(max_length=100, unique=True)
    klass = models.ForeignKey("Klass",related_name="students",on_delete=models.SET_NULL,blank=True,null=True)
    electives = models.ManyToManyField("Subject",related_name="students",blank=True)
    house = models.ForeignKey("House",on_delete=models.SET_NULL,blank=True,null=True)
    bio = models.TextField(null=True, blank=True)
    track = models.ForeignKey(Track,on_delete=models.SET_NULL,null=True,blank=True)
    course = models.ForeignKey("Course",on_delete=models.SET_NULL,null=True,blank=True)
    father = models.CharField(max_length=200, null=True, blank=True)
    mother = models.CharField(max_length=200, null=True, blank=True)
    sms_number = models.CharField(max_length=10, null=True, blank=True)
    completed = models.BooleanField(default=False, db_index=True)
    user = models.OneToOneField(User,related_name="student",on_delete=models.CASCADE)
    last_promotion_date = models.DateField(default=timezone.now)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    relatives = models.ManyToManyField(Relative, related_name="students")
    religion = models.CharField(max_length=200, null=True, blank=True)
    religious_denomination = models.CharField(max_length=200, null=True, blank=True)
    home_town = models.CharField(max_length=100, null=True, blank=True)
    other_tongue = models.CharField(max_length=100, null=True, blank=True)
    last_school_attended = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "students"
        permissions = [
            ('promote_student', 'Can promote students'),
        ]

    def save(self, *args, **kwargs):
        COMPLETE_SCHOOL_DURATION = 3
        if self.klass:
            if not self.start_date:
                self.start_date = datetime.today() - timedelta(
                    days=(self.klass.form - 1) * 365.25)
            if not self.end_date:
                self.end_date = datetime.today() + timedelta(
                    days=COMPLETE_SCHOOL_DURATION -
                    (self.klass.form - 1) * 365.25)
        super().save(*args, **kwargs)

    def my_class(self):
        return self.klass.name

    def class_options(self):
        return Klass.objects.filter(course=self.klass.course)

    def promote(self, step):
        if self.completed: return (True, False)
        final_form = Klass.objects.order_by("-form").first().form
        self.last_promotion_date = timezone.now()
        if self.klass.form + step > final_form:
            self.completed = True
        else:
            new_form = self.klass.form + step
            new_class = Klass.objects.filter(form=new_form,
                                             stream=self.klass.stream,
                                             course=self.klass.course).first()
            if not new_class:
                return False, False
            old_class = self.klass
            self.klass = new_class
            self.completed = False

            # Create history
            session = get_current_session()
            history, _ = StudentPromotionHistory.objects.get_or_create(
                student=self, session=session)
            history.new_class = self.klass
            history.old_class = old_class
            history.save()

        self.save()
        return True, True

    def logo_url(self):
        if self.user:
            return self.user.get_photo_url()
        return "/static/images/default_profile.jpg"

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        if self.user:
            return f"{self.user.get_name()}"
        return f"{self.student_id}"


class Klass(ModelMixin):
    class_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50, unique=True)
    class_teacher = models.ForeignKey("Staff",
                                      related_name="classes",
                                      null=True,
                                      on_delete=models.SET_NULL)
    stage = models.IntegerField(default=1)
    stream = models.CharField(max_length=5)
    course = models.ForeignKey("Course",
                               related_name="classes",
                               on_delete=models.CASCADE)

    def course_name(self):
        return self.course.name

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


class Department(ModelMixin):
    name = models.CharField(max_length=100, unique=True)
    hod = models.ForeignKey("Staff",
                            null=True,
                            blank=True,
                            on_delete=models.SET_NULL)

    class Meta:
        db_table = "departments"

    def __str__(self):
        return self.name


class Course(ModelMixin):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, unique=True)
    subjects = models.ManyToManyField("Subject", related_name="courses")
    hod = models.ForeignKey("Staff",
                            null=True,
                            blank=True,
                            on_delete=models.SET_NULL)

    class Meta:
        db_table = "courses"

    def __str__(self):
        return self.name

    def get_number_of_students(self):
        num = 0
        for klass in self.classes.all():
            num += klass.get_student_count()
        return num


class Subject(ModelMixin):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, unique=True)
    department = models.ForeignKey("Department",
                                   related_name="subjects",
                                   null=True,
                                   blank=True,
                                   on_delete=models.CASCADE)

    class Meta:
        db_table = "subjects"

    def __str__(self):
        return self.name

    def get_number_of_students(self):
        num = 0
        for klass in self.courses.all():
            num += klass.get_student_count()
        return num

    is_elective = models.BooleanField()

    class Meta:
        db_table = "subjects"

    def student_count(self):
        if self.is_elective:
            return Student.objects.filter(completed=False,
                                          electives=self).count()
        return Student.objects.filter(completed=False).count()

    def __str__(self):
        return self.name

    def get_number_of_students(self):
        return self.students.all().count()


class Staff(ModelMixin):
    staff_id = models.CharField(max_length=100, unique=True)
    has_left = models.BooleanField(default=False)
    teaching = models.BooleanField(default=True)
    user = models.OneToOneField(User,
                                related_name="staff",
                                on_delete=models.CASCADE)

    class Meta:
        db_table = "staff"
        verbose_name_plural = "Staff"

    def __str__(self):
        return f"{self.staff_id}"

    def get_full_name(self):
        return f"{self.surname} {self.other_names}"

    def get_number_of_students(self):
        number = 0
        if hasattr(self, "teaches"):
            for item in self.teaches.all():
                number += item.subject.students.all().count()
        return number


class Record(ModelMixin):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    klass = models.ForeignKey(Klass,
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True)
    exam_score = models.IntegerField(default=0, blank=True, null=True)
    class_score = models.IntegerField(default=0, blank=True, null=True)
    total_exam_score = models.IntegerField(default=100, blank=True, null=True)
    total_class_score = models.IntegerField(default=100, blank=True, null=True)
    total = models.IntegerField(default=0, blank=True, null=True)
    subject = models.ForeignKey("Subject", on_delete=models.PROTECT)
    updated_by = models.ForeignKey(User,
                                   blank=True,
                                   null=True,
                                   related_name="records",
                                   on_delete=models.PROTECT)
    grade = models.CharField(max_length=5, blank=True, null=True)
    remark = models.CharField(max_length=20, blank=True, null=True)
    session = models.ForeignKey(SchoolSession,
                                on_delete=models.SET_NULL,
                                null=True)
    group_tag = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    roll_no = models.IntegerField(blank=True, null=True)
    position = models.IntegerField(null=True, blank=True)

    class Meta:
        permissions = [
            ('manage_other_record',
             'Can add/change academic/classwork records of other teachers'),
        ]
        db_table = "academic_records"

    def __str__(self):
        return self.student.get_full_name()

    @property
    def rank(self):
        return f"{self.position}/{self.roll_no}"

    def save(self, *args, **kwargs):
        if self.class_score and self.exam_score and self.total_class_score and self.total_exam_score:
            self.total = round(
                30 * float(self.class_score / self.total_class_score) +
                70 * float(self.exam_score / self.total_exam_score))

            grading_system = GradingSystem.objects.filter(
                min_score__lte=self.total).order_by("-min_score").first()
            if grading_system:
                self.grade = grading_system.grade
                self.remark = grading_system.remark
            else:
                self.grade = "F"
                self.remark = "Fail"
        super(Record, self).save(*args, **kwargs)

    def compute_position(self):
        totals = set()
        records = Record.objects.filter(group_tag=self.group_tag)
        for record in records:
            totals.add(record.total)
        totals = sorted(list(totals))

        for record in records:
            record.position =  totals.index(record.total) + 1
            record.roll_no = len(records)
            record.save()


class SubjectMapping(ModelMixin):
    subject = models.ForeignKey("Subject",
                                on_delete=models.CASCADE,
                                related_name="teachers")
    klass = models.ForeignKey("Klass",
                              verbose_name="Class",
                              related_name="combinations",
                              on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff,
                              related_name="teaches",
                              verbose_name="Staff",
                              null=True,
                              blank=True,
                              on_delete=models.CASCADE)
    session = models.ForeignKey(SchoolSession, on_delete=models.CASCADE)

    class Meta:
        db_table = "subject_mapping"

    def subject_name(self):
        return self.subject.name

    def class_name(self):
        return self.klass.name

    def teacher(self):
        return self.staff.get_full_name()

    def __str__(self):
        if self.subject and self.staff:
            return "{} - {}: {}".format(self.subject.name.capitalize(),
                                        self.klass.name,
                                        self.staff.user.get_name())
        else:
            return str(self.id)


class SessionReport(ModelMixin):
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    session = models.ForeignKey(SchoolSession,
                                on_delete=models.SET_NULL,
                                null=True)
    klass = models.ForeignKey("Klass",
                              null=True,
                              blank=True,
                              on_delete=models.CASCADE)
    attendance = models.IntegerField(default=0, null=True, blank=True)
    total_attendance = models.IntegerField(default=0, null=True, blank=True)
    attitude = models.ForeignKey(Attitude,
                                 null=True,
                                 blank=True,
                                 on_delete=models.PROTECT)
    interest = models.ForeignKey(Interest,
                                 null=True,
                                 blank=True,
                                 on_delete=models.PROTECT)
    conduct = models.ForeignKey(Conduct,
                                null=True,
                                blank=True,
                                on_delete=models.PROTECT)
    assistant_head_signature = models.ImageField(
        upload_to="uploads/signatures", null=True, blank=True)
    signed_by = models.ForeignKey(Staff,
                                  on_delete=models.PROTECT,
                                  null=True,
                                  blank=True)
    class_teacher_remark = models.ForeignKey(Remark,
                                             null=True,
                                             blank=True,
                                             on_delete=models.PROTECT)
    house_master_remark = models.ForeignKey(Remark,
                                            null=True,
                                            blank=True,
                                            related_name="house_master_remark",
                                            on_delete=models.PROTECT)
    promotion = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = "class_teacher_report"
        permissions = [
            ('manage_other_report', 'Can manage reports of other classes.'),
            ('manage_class_teacher_report',
             'Can manage class teacher report.'),
            ('manage_house_master_report', 'Can manage house master report.'),
            ('append_assistance_head_signature',
             'Can append assistance head signature.'),
        ]

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.session.name}"

    def signature_url(self):
        if self.assistant_head_signature:
            return self.assistant_head_signature.url
        else:
            return ""


class House(ModelMixin):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    house_master = models.ForeignKey("Staff",
                                     on_delete=models.SET_NULL,
                                     null=True)

    class Meta:
        db_table = "houses"

    def __str__(self):
        return self.name


class StudentPromotionHistory(ModelMixin):
    student = models.ForeignKey("Student",
                                related_name="promotion_histories",
                                on_delete=models.CASCADE)
    new_class = models.ForeignKey("Klass",
                                  blank=True,
                                  null=True,
                                  related_name="new_classes",
                                  on_delete=models.CASCADE)
    old_class = models.ForeignKey("Klass",
                                  blank=True,
                                  null=True,
                                  related_name="old_classes",
                                  on_delete=models.CASCADE)
    session = models.ForeignKey(SchoolSession,
                                on_delete=models.SET_NULL,
                                null=True)
    class Meta:
        db_table = "student_promotion_history"

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.new_class} {self.old_class}"


class Notification(models.Model):
    PURPOSE_CHOICES = [
        ("PIN_RESET","PIN_RESET"),
        ("REPORT","REPORT"),
        ("GENERAL","GENERAL"),
    ]
    text = models.TextField()
    id_tag = models.CharField(max_length=50,null=True, blank=True)
    sender_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100)
    destination = models.CharField(max_length=50)
    type = models.CharField(max_length=50,default="sms")
    purpose = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    initiated_by = models.ForeignKey(User, on_delete=models.PROTECT)
    response_data = models.TextField(null=True, blank=True)

    def send(self):
        from setup.models import School

        message = self.text
        phone = "233" + self.destination[1:]
        sender_id = School.objects.first().sms_sender_id

        api_key = settings.ARKESEL_API_KEY
        if not (api_key and sender_id): return

        message = message.replace(" ", "+")

        url = f"https://sms.arkesel.com/sms/api?action=send-sms&api_key={api_key}&to={phone}&from={sender_id}&sms={message}"
        response = requests.get(url)
        self.response_data = response.text

        if response.json().get("code", "").lower() == "ok":
            self.status = "delivered"
        else:
            self.status = "failed"

        self.save()