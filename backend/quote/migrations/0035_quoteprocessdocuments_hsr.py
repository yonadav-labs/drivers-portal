# Generated by Django 2.2.10 on 2020-02-19 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hellosign_app', '0001_initial'),
        ('quote', '0034_auto_20200213_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='quoteprocessdocuments',
            name='hsr',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hellosign_app.HelloSignSignatureRequest', verbose_name='HelloSign Request'),
        ),
    ]
