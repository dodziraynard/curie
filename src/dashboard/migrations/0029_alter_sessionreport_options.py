# Generated by Django 3.2.11 on 2022-07-19 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0028_auto_20220719_0926'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sessionreport',
            options={'permissions': [('manage_other_report', 'Can manage reports of other classes.'), ('manage_class_teacher_report', 'Can manage class teacher report.'), ('manage_house_master_report', 'Can manage house master report.')]},
        ),
    ]
