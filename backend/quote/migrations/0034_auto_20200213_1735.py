# Generated by Django 2.2.9 on 2020-02-13 17:35

from django.db import migrations, models
import quote.models


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0033_quoteprocess_is_hereford'),
    ]

    operations = [
        migrations.AddField(
            model_name='quoteprocessdocuments',
            name='loss_run',
            field=models.FileField(blank=True, null=True, upload_to=quote.models.quote_process_document_upload_to, verbose_name='Loss Run Document'),
        ),
        migrations.AddField(
            model_name='quoteprocessdocuments',
            name='vehicle_title',
            field=models.FileField(blank=True, null=True, upload_to=quote.models.quote_process_document_upload_to, verbose_name='Vehicle Title or Bill of Sale or MV-50'),
        ),
    ]
