# Generated by Django 3.0.2 on 2020-02-09 04:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('powerball', '0002_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='picture',
            name='thumb',
        ),
    ]
