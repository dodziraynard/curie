# Generated by Django 4.1.7 on 2023-04-01 14:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dashboard', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('setup', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectmapping',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='setup.schoolsession'),
        ),
        migrations.AddField(
            model_name='subjectmapping',
            name='staff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teaches', to='dashboard.staff', verbose_name='Staff'),
        ),
        migrations.AddField(
            model_name='subjectmapping',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teachers', to='dashboard.subject'),
        ),
        migrations.AddField(
            model_name='subject',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='dashboard.department'),
        ),
        migrations.AddField(
            model_name='studentpromotionhistory',
            name='new_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='new_classes', to='dashboard.klass'),
        ),
        migrations.AddField(
            model_name='studentpromotionhistory',
            name='old_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='old_classes', to='dashboard.klass'),
        ),
        migrations.AddField(
            model_name='studentpromotionhistory',
            name='session',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='setup.schoolsession'),
        ),
        migrations.AddField(
            model_name='studentpromotionhistory',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='promotion_histories', to='dashboard.student'),
        ),
        migrations.AddField(
            model_name='student',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.course'),
        ),
        migrations.AddField(
            model_name='student',
            name='electives',
            field=models.ManyToManyField(blank=True, related_name='students', to='dashboard.subject'),
        ),
        migrations.AddField(
            model_name='student',
            name='house',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.house'),
        ),
        migrations.AddField(
            model_name='student',
            name='klass',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='dashboard.klass'),
        ),
        migrations.AddField(
            model_name='student',
            name='track',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='setup.track'),
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='staff',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='staff', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sessionreport',
            name='attitude',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='setup.attitude'),
        ),
        migrations.AddField(
            model_name='sessionreport',
            name='class_teacher_remark',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='setup.remark'),
        ),
        migrations.AddField(
            model_name='sessionreport',
            name='conduct',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='setup.conduct'),
        ),
        migrations.AddField(
            model_name='sessionreport',
            name='house_master_remark',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='house_master_remark', to='setup.remark'),
        ),
        migrations.AddField(
            model_name='sessionreport',
            name='interest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='setup.interest'),
        ),
        migrations.AddField(
            model_name='sessionreport',
            name='klass',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.klass'),
        ),
        migrations.AddField(
            model_name='sessionreport',
            name='session',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='setup.schoolsession'),
        ),
        migrations.AddField(
            model_name='sessionreport',
            name='signed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='dashboard.staff'),
        ),
        migrations.AddField(
            model_name='sessionreport',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.student'),
        ),
        migrations.AddField(
            model_name='record',
            name='klass',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.klass'),
        ),
        migrations.AddField(
            model_name='record',
            name='session',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='setup.schoolsession'),
        ),
        migrations.AddField(
            model_name='record',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.student'),
        ),
        migrations.AddField(
            model_name='record',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dashboard.subject'),
        ),
        migrations.AddField(
            model_name='record',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='records', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='klass',
            name='class_teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='classes', to='dashboard.staff'),
        ),
        migrations.AddField(
            model_name='klass',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='dashboard.course'),
        ),
        migrations.AddField(
            model_name='house',
            name='house_master',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.staff'),
        ),
        migrations.AddField(
            model_name='department',
            name='hod',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.staff'),
        ),
        migrations.AddField(
            model_name='course',
            name='hod',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dashboard.staff'),
        ),
        migrations.AddField(
            model_name='course',
            name='subjects',
            field=models.ManyToManyField(related_name='courses', to='dashboard.subject'),
        ),
    ]
