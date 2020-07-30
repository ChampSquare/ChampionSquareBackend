# Generated by Django 2.2 on 2020-07-30 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20200727_2316'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answerpaper',
            options={'ordering': ['-created_at'], 'verbose_name': 'AnswerPaper', 'verbose_name_plural': 'AnswerPapers'},
        ),
        migrations.AddField(
            model_name='answerpaper',
            name='user_ip',
            field=models.GenericIPAddressField(blank=True, null=True, verbose_name='IP address of user'),
        ),
    ]