# Generated by Django 3.2.4 on 2021-07-07 06:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_alter_message_sent_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sent_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]