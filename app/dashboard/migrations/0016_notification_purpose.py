# Generated by Django 4.1.7 on 2023-04-03 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0015_remove_record_rank_student_sms_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='purpose',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
