# Generated by Django 3.2.11 on 2022-07-10 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conduct',
            old_name='name',
            new_name='text',
        ),
        migrations.RenameField(
            model_name='interest',
            old_name='name',
            new_name='text',
        ),
        migrations.RenameField(
            model_name='track',
            old_name='name',
            new_name='text',
        ),
    ]
