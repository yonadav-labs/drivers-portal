# Generated by Django 2.2.9 on 2020-02-02 11:40

from django.db import migrations
import users.managers


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManualQuoteUser',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('users.user',),
            managers=[
                ('objects', users.managers.UserManager()),
            ],
        ),
    ]