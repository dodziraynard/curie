from django.db import models
from accounts.models import User
from django.utils import timezone

from setup.models import GradingSystem, ModelMixin, Track, Attitude, Conduct, Interest, SchoolSession


class Student(ModelMixin):
    student_id = models.CharField(max_length=100, unique=True)
    klass = models.ForeignKey("Klass",
                              related_name="students",
                              on_delete=models.SET_NULL,
                              null=True)
    electives = models.ManyToManyField("Subject",
                                       related_name="students",
                                       blank=True)
    house = models.ForeignKey("House", on_delete=models.SET_NULL, null=True)
    bio = models.TextField(null=True, blank=True)
    track = models.ForeignKey(Track,
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True)
    father = models.CharField(max_length=200, null=True, blank=True)
    mother = models.CharField(max_length=200, null=True, blank=True)
    completed = models.BooleanField(default=False)
    user = models.OneToOneField(User,
                                related_name="student",
                                on_delete=models.CASCADE)
    last_promotion_date = models.DateField(default=timezone.now)

    def my_class(self):
        return self.klass.name

    def promote(self):
        final_form = Klass.objects.order_by("-form").first().form
        self.last_promotion_date = timezone.now()
        if self.klass.form >= final_form:
            self.completed = True
        else:
            next_form = self.klass.form + 1
            next_class = Klass.objects.get(form=next_form,
                                           stream=self.klass.stream,
                                           course=self.klass.course)
            self.klass = next_class
        self.save()

    class Meta:
        db_table = "students"

    def __str__(self):
        return f"{self.surname} {self.other_names}"

    def get_full_name(self):
        return f"{self.surname} {self.other_names}"


class Klass(ModelMixin):
    class_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50, unique=True)
    class_teacher = models.OneToOneField("Staff",
                                         related_name="klass",
                                         null=True,
                                         on_delete=models.SET_NULL)
    form = models.IntegerField(default=1)
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
        ordering = ['name']
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
        ordering = ['name']
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
        ordering = ['name']
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
    department = models.ForeignKey("Staff",
                                   related_name="subjects",
                                   null=True,
                                   blank=True,
                                   on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
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
        ordering = ['name']
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
    exam_score = models.IntegerField(default=0, blank=True, null=True)
    class_score = models.IntegerField(default=0, blank=True, null=True)
    total = models.IntegerField(default=0, blank=True, null=True)
    subject = models.ForeignKey("Subject", on_delete=models.PROTECT)
    uploaded_by = models.ForeignKey(Staff,
                                    related_name="records",
                                    on_delete=models.PROTECT)
    klass = models.ForeignKey("Klass", on_delete=models.CASCADE)
    grade = models.CharField(max_length=5, blank=True, null=True)
    remark = models.CharField(max_length=20, blank=True, null=True)
    position = models.CharField(max_length=5, blank=True, null=True)
    session = models.ForeignKey(SchoolSession,
                                on_delete=models.SET_NULL,
                                null=True)
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


class SubjectAssignment(ModelMixin):
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
                              on_delete=models.CASCADE)

    class Meta:
        db_table = "subject_assignment"

    def subject_name(self):
        return self.subject.name

    def class_name(self):
        return self.klass.name

    def teacher(self):
        return self.staff.get_full_name()

    def __str__(self):
        if self.subject and self.staff:
            return "{} - {}: {}".format(self.subject.name.capitalize(),
                                        self.klass.name, self.staff.surname)
        else:
            return str(self.id)


class ClassTeacherRemark(ModelMixin):
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    session = models.ForeignKey(SchoolSession,
                                on_delete=models.SET_NULL,
                                null=True)
    klass = models.ForeignKey("klass", on_delete=models.CASCADE)
    attendance = models.IntegerField(default=0)
    total_attendance = models.IntegerField(default=0)
    attitude = models.ForeignKey(Attitude, on_delete=models.CASCADE)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
    conduct = models.ForeignKey(Conduct, on_delete=models.CASCADE)
    remark = models.CharField(max_length=200)

    class Meta:
        db_table = "class_teacher_remarks"

    def __str__(self):
        return f"{self.student.surname} - {self.semester} {self.academic_year}"


class HouseMasterRemark(ModelMixin):
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    staff = models.ForeignKey("Staff", on_delete=models.CASCADE)
    session = models.ForeignKey(SchoolSession,
                                on_delete=models.SET_NULL,
                                null=True)
    remark = models.CharField(max_length=200)
    klass = models.ForeignKey("Klass", on_delete=models.CASCADE)

    class Meta:
        db_table = "house_master_remarks"

    def __str__(self):
        return f"{self.student.surname} - {self.semester} {self.academic_year}"


class House(ModelMixin):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    house_master = models.ForeignKey("Staff",
                                     on_delete=models.SET_NULL,
                                     null=True)

    class Meta:
        ordering = ['name']
        db_table = "houses"

    def __str__(self):
        return f"{self.student.surname} - {self.semester} {self.academic_year}"
