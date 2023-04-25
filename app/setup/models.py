from datetime import datetime

from django.db import models
from django.utils import timezone


class ModelMixin(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def model_name(self):
        return self.__class__.__name__.lower()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


# Just for permissions
class SetupPerms(models.Model):

    class Meta:
        managed = False  # No database table creation or deletion  \
        # operations will be performed for this model.
        default_permissions = ()  # disable "add", "change", "delete"
        # and "view" default permissions
        permissions = [
            ('manage_setup', 'Can manage system setup'),
            ('view_dashboard', 'Can view dashboard'),
            ('manage_action_center', 'Can view dashboard'),

            ("view_student", "Can view student"),
            ("add_student", "Can add student"),
            ("change_student", "Can change student"),
            ("delete_student", "Can delete student"),
            ("view_staff", "Can view staff"),
            ("add_staff", "Can add staff"),
            ("change_staff", "Can change staff"),
            ("delete_staff", "Can delete staff"),
            ("view_class", "Can view class"),
            ("add_class", "Can add class"),
            ("change_class", "Can change class"),
            ("delete_class", "Can delete class"),
            ("view_subject", "Can view subject"),
            ("add_subject", "Can add subject"),
            ("change_subject", "Can change subject"),
            ("delete_subject", "Can delete subject"),
            ("view_department", "Can view department"),
            ("add_department", "Can add department"),
            ("change_department", "Can change department"),
            ("delete_department", "Can delete department"),
            ("view_house", "Can view house"),
            ("add_house", "Can add house"),
            ("change_house", "Can change house"),
            ("delete_house", "Can delete house"),

            # Accounting
            ('view_accounting', 'Can access accounting menu'),
            # Invoices
            ("view_invoice", "Can view invoice"),
            ("add_invoice", "Can add invoice"),
            ("change_invoice", "Can change invoice"),
            ("apply_invoice", "Can apply invoice"),
            ("delete_invoice", "Can delete invoice"),

            # Invoice items
            ("view_invoiceitem", "Can view invoice item"),
            ("add_invoiceitem", "Can add invoice item"),
            ("change_invoiceitem", "Can change invoice item"),
            ("delete_invoiceitem", "Can delete invoice item"),

            # Alert
            ('view_alert', 'Can access alert menu'),
            ('compose_sms', 'Can compose sms'),
            ('send_pin_notification', 'Can send pin notification'),
            ('send_report_notification', 'Can send report notification'),
            ('view_notification_history', 'Can view notification history'),

            # Reporting
            ('view_reporting', 'Can access reporting menu'),
            ('generate_limited_report', 'Can access reporting menu'),
        ]


class SchoolSession(ModelMixin):
    name = models.CharField(max_length=50)
    semester = models.IntegerField(verbose_name="Semester/Term")
    academic_year = models.CharField(max_length=10)
    tracks = models.ManyToManyField("Track", blank=True)
    start_date = models.DateField(verbose_name="Start Date",
                                  null=True,
                                  blank=True)
    end_date = models.DateField(verbose_name="End Date", null=True, blank=True)

    class Meta:
        db_table = "school_sessions"

    def __str__(self):
        return self.name

    def active(self):
        return self.start_date <= datetime.today().date() <= self.end_date


class Track(ModelMixin):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Attitude(ModelMixin):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Conduct(ModelMixin):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Interest(ModelMixin):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Remark(ModelMixin):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class GradingSystem(ModelMixin):
    min_score = models.IntegerField(unique=True)
    grade = models.CharField(max_length=2)
    remark = models.CharField(max_length=50)

    class Meta:
        ordering = ["-min_score"]
        db_table = "grading_systems"

    def __str__(self):
        return f"{self.min_score} - {self.grade} - {self.remark}"


class School(ModelMixin):
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    email_address = models.EmailField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to="school_logos", blank=True, null=True)
    head_teacher = models.OneToOneField("dashboard.Staff",
                                        null=True,
                                        blank=True,
                                        on_delete=models.SET_NULL)
    assistant_head_teacher = models.OneToOneField(
        "dashboard.Staff",
        related_name="assistance_school",
        null=True,
        blank=True,
        on_delete=models.SET_NULL)
    current_session = models.ForeignKey(SchoolSession,
                                        on_delete=models.SET_NULL,
                                        null=True,
                                        blank=True)
    current_track = models.ForeignKey(Track,
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      blank=True)
    sms_sender_id = models.CharField(max_length=255, blank=True, null=True)
    sms_active = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "schools"

    def __str__(self):
        return self.name

    def logo_url(self):
        if self.logo:
            return self.logo.url
        return ""

    def get_current_session(self):
        if self.current_session:
            return self.current_session
        return SchoolSession.objects.filter(
            date_start__lte=timezone.now()).order_by("-date_start").first()

    def get_logo_url(self):
        if self.logo:
            return self.logo.url
        return "/static/images/logo.png"
