# Generated by Django 4.1.7 on 2023-04-02 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relative',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('username', models.CharField(max_length=100)),
                ('fullname', models.CharField(max_length=200)),
                ('address', models.TextField(blank=True, null=True)),
                ('occupation', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=10, null=True)),
                ('education', models.CharField(blank=True, max_length=100, null=True)),
                ('religion', models.CharField(blank=True, max_length=100, null=True)),
                ('spouses', models.IntegerField()),
                ('date_of_demise', models.DateField(blank=True, null=True)),
                ('relationship', models.CharField(choices=[('mother', 'mother'), ('father', 'father'), ('guardian', 'guardian')], max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='student',
            name='dob',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='hometown',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='last_school_attended',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='other_tongue',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='religion',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='religious_denomination',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='relatives',
            field=models.ManyToManyField(related_name='students', to='dashboard.relative'),
        ),
    ]
