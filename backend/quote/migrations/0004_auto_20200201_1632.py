# Generated by Django 2.2.9 on 2020-02-01 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0003_auto_20200201_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quoteprocess',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Email'),
        ),
    ]
