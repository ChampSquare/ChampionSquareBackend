# Generated by Django 2.2 on 2020-06-04 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Uscholar', '0004_auto_20200604_0925'),
    ]

    operations = [
        migrations.AddField(
            model_name='videorecord',
            name='rec_file_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]