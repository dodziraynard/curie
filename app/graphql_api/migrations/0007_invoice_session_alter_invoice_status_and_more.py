# Generated by Django 4.1.7 on 2023-04-09 03:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0006_alter_setupperms_options'),
        ('graphql_api', '0006_alter_invoice_status_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='setup.schoolsession'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.CharField(choices=[('applied', 'applied'), ('draft', 'draft'), ('pending', 'pending')], max_length=100),
        ),
        migrations.AlterField(
            model_name='invoiceitem',
            name='type',
            field=models.CharField(choices=[('debit', 'debit'), ('credit', 'credit')], max_length=100),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='direction',
            field=models.CharField(choices=[('in', 'in'), ('out', 'out')], max_length=10),
        ),
    ]
