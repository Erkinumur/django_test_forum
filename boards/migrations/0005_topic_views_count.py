# Generated by Django 2.2 on 2020-06-04 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0004_auto_20200528_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='views_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
