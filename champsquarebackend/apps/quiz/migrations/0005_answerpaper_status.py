# Generated by Django 2.2 on 2020-07-22 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20200722_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='answerpaper',
            name='status',
            field=models.CharField(blank=True, max_length=32, verbose_name='Status of Test'),
        ),
    ]
