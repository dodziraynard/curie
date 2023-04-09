# Generated by Django 4.1.7 on 2023-04-08 23:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('graphql_api', '0004_rename_description_invoice_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceitem',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='created_invoice_items', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoiceitem',
            name='updated_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='updated_invoice_items', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invoiceitem',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_items', to='graphql_api.invoice'),
        ),
    ]
