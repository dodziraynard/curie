# Generated by Django 3.2.11 on 2022-07-18 23:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0009_auto_20220711_1548'),
        ('dashboard', '0017_auto_20220718_2304'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentPromotionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('klass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.klass')),
                ('session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='setup.schoolsession')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.student')),
            ],
            options={
                'db_table': 'student_promotion_history',
            },
        ),
    ]
