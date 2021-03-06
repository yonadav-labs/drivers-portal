# Generated by Django 2.2.9 on 2020-02-09 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0017_auto_20200209_0929'),
    ]

    operations = [
        migrations.AddField(
            model_name='quoteprocess',
            name='status',
            field=models.CharField(choices=[('created', 'Created'), ('docs', 'Docs Pending'), ('review', 'Docs Submitted'), ('payment', 'Payment Pending'), ('paid', 'Payment Done'), ('done', 'Done')], default='created', max_length=7),
        ),
    ]
