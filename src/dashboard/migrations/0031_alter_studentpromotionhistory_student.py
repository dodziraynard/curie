# Generated by Django 3.2.11 on 2022-07-19 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0030_auto_20220719_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentpromotionhistory',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='promotion_histories', to='dashboard.student'),
        ),
    ]