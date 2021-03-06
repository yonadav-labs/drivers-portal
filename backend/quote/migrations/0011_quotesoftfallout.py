# Generated by Django 2.2.10 on 2020-02-06 11:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0010_quoteprocess_fault_accidents_last_months'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuoteSoftFallout',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified date')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('phone_number', models.CharField(max_length=255, verbose_name='Phone Number')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
            ],
            options={
                'verbose_name': 'Quote Soft Fallout',
                'verbose_name_plural': 'Quote Soft Fallouts',
                'ordering': ('-created',),
            },
        ),
    ]
