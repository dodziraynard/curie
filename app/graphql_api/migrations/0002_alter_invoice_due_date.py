# Generated by Django 4.1.7 on 2023-04-02 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graphql_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]