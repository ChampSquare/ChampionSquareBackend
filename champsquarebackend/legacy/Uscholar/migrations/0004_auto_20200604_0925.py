# Generated by Django 2.2 on 2020-06-04 03:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Uscholar', '0003_auto_20200604_0923'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videorecord',
            name='audio_file_name',
        ),
        migrations.RemoveField(
            model_name='videorecord',
            name='video_file_name',
        ),
    ]
