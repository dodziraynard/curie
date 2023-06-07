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


# Just for permissions
class SetupPerms(models.Model):

    class Meta:
        managed = False
        default_permissions = ()
        permissions = [
            ('manage_setup', 'Can manage system setup'),
            ('manage_users', 'Can manage system users'),
            ('view_dashboard', 'Can view dashboard'),
            ("manage_other_report", "Can manage reports others"),
            ("manage_roles", "Can manage roles"),

            # Action center
            ('view_action_center', 'Can view action center'),
            ('manage_action_center', 'Can manage action center'),

            # Subject mapping
            ('add_subject_mapping', 'Can add subject mapping'),
            ('view_subject_mapping', 'Can view subject mapping'),

            # Promotion
            ('view_promotion', 'Can view promotion'),
            ('add_promotion', 'Can add promotion'),
            ('revert_promotion', 'Can revert promotion'),

            # Class teacher
            ('change_class_teacher_remark', 'Can change class teacher remark'),

            # House master
            ('change_house_master_remark', 'Can change house master remark'),

            # Assisant head
            ('append_signature', 'Can append signature to reports'),

            # Academic records
            ('change_academic_record', 'Can change academic records'),

            ###### ENTITIES ######
            # User
            ("view_user", "Can view user"),
            ("add_user", "Can add user"),
            ("change_user", "Can change user"),
            ("delete_user", "Can delete user"),

            # Student
            ("view_student", "Can view student"),
            ("add_student", "Can add student"),
            ("change_student", "Can change student"),
            ("delete_student", "Can delete student"),

            # Staff
            ("view_staff", "Can view staff"),
            ("add_staff", "Can add staff"),
            ("change_staff", "Can change staff"),
            ("delete_staff", "Can delete staff"),

            # Class
            ("view_class", "Can view class"),
            ("add_class", "Can add class"),
            ("change_class", "Can change class"),
            ("delete_class", "Can delete class"),

            # Subject
            ("view_subject", "Can view subject"),
            ("add_subject", "Can add subject"),
            ("change_subject", "Can change subject"),
            ("delete_subject", "Can delete subject"),

            # Course
            ("view_course", "Can view course"),
            ("add_course", "Can add course"),
            ("change_course", "Can change course"),
            ("delete_course", "Can delete course"),

            # Department
            ("view_department", "Can view department"),
            ("add_department", "Can add department"),
            ("change_department", "Can change department"),
            ("delete_department", "Can delete department"),

            # House
            ("view_house", "Can view house"),
            ("add_house", "Can add house"),
            ("change_house", "Can change house"),
            ("delete_house", "Can delete house"),

            # Attitude
            ("view_attitude", "Can view attitude"),
            ("add_attitude", "Can add attitude"),
            ("change_attitude", "Can change attitude"),
            ("delete_attitude", "Can delete attitude"),

            # Conduct
            ("view_conduct", "Can view conduct"),
            ("add_conduct", "Can add conduct"),
            ("change_conduct", "Can change conduct"),
            ("delete_conduct", "Can delete conduct"),

            # Interest
            ("view_interest", "Can view interest"),
            ("add_interest", "Can add interest"),
            ("change_interest", "Can change interest"),
            ("delete_interest", "Can delete interest"),

            # Track
            ("view_track", "Can view track"),
            ("add_track", "Can add track"),
            ("change_track", "Can change track"),
            ("delete_track", "Can delete track"),

            # Remark
            ("view_remark", "Can view remark"),
            ("add_remark", "Can add remark"),
            ("change_remark", "Can change remark"),
            ("delete_remark", "Can delete remark"),

            # School session
            ("view_schooolsession", "Can view schooolsession"),
            ("add_schooolsession", "Can add schooolsession"),
            ("change_schooolsession", "Can change schooolsession"),
            ("delete_schooolsession", "Can delete schooolsession"),

            # Grading system
            ("view_gradingsystem", "Can view gradingsystem"),
            ("add_gradingsystem", "Can add gradingsystem"),
            ("change_gradingsystem", "Can change gradingsystem"),
            ("delete_gradingsystem", "Can delete schooolsession"),

            # ACCOUNTING
            ('view_accounting', 'Can access accounting menu'),
            # Invoices
            ("view_invoice", "Can view invoice"),
            ("add_invoice", "Can add invoice"),
            ("change_invoice", "Can change invoice"),
            ("apply_invoice", "Can apply invoice"),
            ("delete_invoice", "Can delete invoice"),

            # Invoices
            ("view_invoiceitem", "Can view invoice item"),
            ("add_invoiceitem", "Can add invoice item"),
            ("change_invoiceitem", "Can change invoice item"),
            ("delete_invoiceitem", "Can delete invoice item"),

            # Paymnet
            ("view_payment", "Can view payment item"),
            ("add_payment", "Can add payment item"),
            ("change_payment", "Can change payment item"),
            ("delete_payment", "Can delete payment item"),

            # Alert
            ('view_alert', 'Can access alert menu'),
            ('compose_sms', 'Can compose sms'),
            ('send_pin_notification', 'Can send pin notification'),
            ('send_report_notification', 'Can send report notification'),
            ('resend_notification', 'Can resend notifications'),
            ('view_notification_history', 'Can view notification history'),

            # Reporting
            ('view_reporting', 'Can access reporting menu'),
            ('generate_limited_report', 'Can access reporting menu'),

            # Inventory
            ("view_inventory", "Can view inventory"),
            ("add_inventory", "Can add inventory"),
            ("change_inventory", "Can change inventory"),
            ("delete_inventory", "Can delete inventory"),

            # Inventory
            ("view_issuance", "Can view issuance"),
            ("add_issuance", "Can add issuance"),
            ("change_issuance", "Can change issuance"),
            ("delete_issuance", "Can delete issuance"),

            # Personal permissions
            ("view_personal_academic_record",
             "Can view personal academic record"),
            ("view_personal_invoice", "Can view personal invoice"),
            ("view_personal_payment_history",
             "Can view personal payment history"),
        ]


class SchoolSession(ModelMixin):
    name = models.CharField(max_length=50)
    semester = models.IntegerField(verbose_name="Semester/Term")
    academic_year = models.CharField(max_length=10)
    tracks = models.ManyToManyField("Track", blank=True)
    start_date = models.DateField(verbose_name="Start Date",
                                  null=True,
                                  blank=True)
    next_start_date = models.DateField(verbose_name="Next Date",
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
    sms_balance = models.IntegerField(default=0)
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
