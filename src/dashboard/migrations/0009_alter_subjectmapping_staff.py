# Generated by Django 3.2.11 on 2022-07-12 23:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_subjectmapping_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subjectmapping',
            name='staff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teaches', to='dashboard.staff', verbose_name='Staff'),
        ),
    ]