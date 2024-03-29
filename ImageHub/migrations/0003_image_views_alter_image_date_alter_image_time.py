# Generated by Django 4.2 on 2023-05-09 10:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ImageHub', '0002_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='views',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='image',
            name='date',
            field=models.DateField(default=datetime.date(2023, 5, 9)),
        ),
        migrations.AlterField(
            model_name='image',
            name='time',
            field=models.TimeField(default=datetime.time(10, 17, 27, 483508)),
        ),
    ]
