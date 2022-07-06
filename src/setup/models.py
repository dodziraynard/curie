from django.db import models


class ModelMixin(models.Model):
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
            ('view_dashboard', 'Can view application dashboard'),
        ]


class SchoolSession(ModelMixin):
    name = models.CharField(max_length=50)
    semester = models.IntegerField(verbose_name="Semester/Term")
    academic_year = models.CharField(max_length=10)

    class Meta:
        db_table = "school_sessions"

    def __str__(self):
        return f"{self.min_score} - {self.grade} - {self.remark}"


class Attitude(ModelMixin):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Conduct(ModelMixin):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Interest(ModelMixin):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Track(ModelMixin):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class GradingSystem(models.Model):
    min_score = models.IntegerField()
    grade = models.CharField(max_length=5)
    remark = models.CharField(max_length=50)

    class Meta:
        db_table = "grading_systems"

    def __str__(self):
        return f"{self.min_score} - {self.grade} - {self.remark}"
