# Generated by Django 2.2 on 2020-07-02 19:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20200703_0100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='users',
            field=models.ManyToManyField(blank=True, help_text='User which will be allowed to take test', to=settings.AUTH_USER_MODEL, verbose_name='Users'),
        ),
    ]
