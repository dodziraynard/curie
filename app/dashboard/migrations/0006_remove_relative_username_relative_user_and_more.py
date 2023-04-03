# Generated by Django 4.1.7 on 2023-04-02 11:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0005_rename_form_klass_stage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relative',
            name='username',
        ),
        migrations.AddField(
            model_name='relative',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='relative', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='course',
            name='id',
            field=models.AutoField(default=10000000, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='department',
            name='id',
            field=models.AutoField(default=10000000, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='house',
            name='id',
            field=models.AutoField(default=10000000, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='klass',
            name='id',
            field=models.AutoField(default=10000000, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='id',
            field=models.AutoField(default=10000000, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='relative',
            name='fullname',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='relative',
            name='id',
            field=models.AutoField(default=10000000, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='sessionreport',
            name='id',
            field=models.AutoField(default=10000000, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='staff',
            name='id',
            field=models.AutoField(default=10000000, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='id',
            field=models.AutoField(default=10000000, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='studentpromotionhistory',
            name='id',
            field=models.AutoField(default=10000000, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='id',
            field=models.AutoField(default=10000000, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='subjectmapping',
            name='id',
            field=models.AutoField(default=10000000, primary_key=True, serialize=False, unique=True),
        ),
    ]