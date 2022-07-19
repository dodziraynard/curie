# Generated by Django 3.2.11 on 2022-07-18 23:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0009_auto_20220711_1548'),
        ('dashboard', '0016_record_klass'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassTeacherReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('attendance', models.IntegerField(blank=True, default=0, null=True)),
                ('total_attendance', models.IntegerField(blank=True, default=0, null=True)),
                ('remark', models.CharField(blank=True, max_length=200, null=True)),
                ('promotion', models.CharField(blank=True, max_length=200, null=True)),
                ('attitude', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='setup.attitude')),
                ('conduct', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='setup.conduct')),
                ('interest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='setup.interest')),
                ('klass', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.klass')),
                ('session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='setup.schoolsession')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.student')),
            ],
            options={
                'db_table': 'class_teacher_report',
            },
        ),
        migrations.DeleteModel(
            name='ClassTeacherRemark',
        ),
    ]