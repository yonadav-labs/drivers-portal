# Generated by Django 2.2.9 on 2020-02-08 13:58

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0014_auto_20200208_1331'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuoteProcessVariations',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified date')),
                ('liability_total', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Liability total')),
                ('body_injury', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Body injury')),
                ('property_damage', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Property damage')),
                ('personal_injury_protection', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Personal injury protection')),
                ('aditional_personal_injury_protection', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Aditional personal injury protection')),
                ('uninsured_motorist', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Uninsured motorist')),
                ('physical_total', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Physical total')),
                ('physical_comprehensive', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Physical comprehensive')),
                ('physical_collision', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Physical collision')),
                ('quote_process', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quote.QuoteProcess', verbose_name='Quote Process')),
            ],
            options={
                'verbose_name': 'Quote Process Variations',
                'verbose_name_plural': 'Quote Process Variations',
            },
        ),
    ]