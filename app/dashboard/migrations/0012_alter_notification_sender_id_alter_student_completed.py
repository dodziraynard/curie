# Generated by Django 4.1.7 on 2023-04-03 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='sender_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='completed',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
