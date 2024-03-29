# Generated by Django 4.1.7 on 2023-05-31 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0023_alter_studentpromotionhistory_session'),
        ('graphql_api', '0008_rename_wallet_balances_updated_transaction_account_balances_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceitem',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transaction',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transaction',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='students',
            field=models.ManyToManyField(related_name='invoices', to='dashboard.student'),
        ),
        migrations.AlterField(
            model_name='invoiceitem',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]
