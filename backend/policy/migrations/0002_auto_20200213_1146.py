# Generated by Django 2.2.10 on 2020-02-13 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('policy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='policy',
            name='quote_process',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='quote.QuoteProcess', verbose_name='Quote Process'),
        ),
    ]
