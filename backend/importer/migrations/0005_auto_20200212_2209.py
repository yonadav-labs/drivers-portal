# Generated by Django 2.2.9 on 2020-02-12 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0004_basetype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basetype',
            name='base_number',
            field=models.CharField(db_index=True, max_length=6, verbose_name='Base number'),
        ),
    ]
