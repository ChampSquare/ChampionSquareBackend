# Generated by Django 3.0.5 on 2021-01-09 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participate', '0008_auto_20200801_0311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='otp_code',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Otp code to access test'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='video_monitoring_enabled',
            field=models.BooleanField(default=False, help_text='Turn on/off video monitoring which includes webcam and screen recording', verbose_name='Video Monitoring Enabled?'),
        ),
    ]
