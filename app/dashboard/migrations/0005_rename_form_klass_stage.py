# Generated by Django 4.1.7 on 2023-04-02 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_alter_student_dob'),
    ]

    operations = [
        migrations.RenameField(
            model_name='klass',
            old_name='form',
            new_name='stage',
        ),
    ]
