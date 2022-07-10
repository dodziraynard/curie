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


class Track(ModelMixin):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Attitude(ModelMixin):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Conduct(ModelMixin):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Interest(ModelMixin):
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
