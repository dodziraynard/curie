# Generated by Django 4.1.7 on 2023-04-08 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_notification_purpose'),
        ('graphql_api', '0002_alter_invoice_due_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='student',
        ),
        migrations.AddField(
            model_name='invoice',
            name='students',
            field=models.ManyToManyField(to='dashboard.student'),
        ),
    ]
