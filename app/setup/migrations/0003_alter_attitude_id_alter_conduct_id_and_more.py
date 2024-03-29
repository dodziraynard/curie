# Generated by Django 4.1.7 on 2023-04-02 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0002_alter_attitude_id_alter_conduct_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attitude',
            name='id',
            field=models.AutoField(default=100000, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='conduct',
            name='id',
            field=models.AutoField(default=100000, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='gradingsystem',
            name='id',
            field=models.AutoField(default=100000, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='interest',
            name='id',
            field=models.AutoField(default=100000, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='remark',
            name='id',
            field=models.AutoField(default=100000, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='id',
            field=models.AutoField(default=100000, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='schoolsession',
            name='id',
            field=models.AutoField(default=100000, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='track',
            name='id',
            field=models.AutoField(default=100000, primary_key=True, serialize=False, unique=True),
        ),
    ]
