# Generated by Django 3.2.11 on 2022-07-11 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20220711_1251'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'permissions': [('promote_student', 'Can promote students')]},
        ),
        migrations.CreateModel(
            name='PromotionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('new_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_history', to='dashboard.klass')),
                ('old_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='old_history', to='dashboard.klass')),
            ],
            options={
                'verbose_name_plural': 'Promotion Histories',
            },
        ),
    ]