# Generated by Django 4.1.7 on 2023-04-02 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_alter_course_id_alter_department_id_alter_house_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='hometown',
            new_name='home_town',
        ),
    ]
