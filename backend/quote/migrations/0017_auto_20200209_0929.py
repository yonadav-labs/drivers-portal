# Generated by Django 2.2.9 on 2020-02-09 09:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0016_auto_20200208_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quoteprocess',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]