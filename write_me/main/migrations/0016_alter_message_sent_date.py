# Generated by Django 3.2.4 on 2021-07-07 05:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_message_sent_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sent_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 7, 5, 44, 43, 607174)),
        ),
    ]
