# Generated by Django 3.2.11 on 2022-07-11 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0007_school_current_track'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolsession',
            name='tracks',
            field=models.ManyToManyField(blank=True, to='setup.Track'),
        ),
    ]
