# Generated by Django 2.2 on 2020-07-26 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_auto_20200726_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answerpaper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='quiz.AnswerPaper', verbose_name='AnswerPaper'),
        ),
    ]
