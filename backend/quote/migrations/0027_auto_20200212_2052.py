# Generated by Django 2.2.9 on 2020-02-12 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0026_auto_20200212_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quoteprocess',
            name='accidents_72_months',
            field=models.CharField(blank=True, choices=[('0', '0'), ('1-3', '1-3'), ('4+', '4+')], max_length=3, null=True, verbose_name='Accidents in last 72 months'),
        ),
    ]
