# Generated by Django 2.2 on 2020-07-26 05:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('participate', '0003_participant_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0001_initial'),
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='participants', through='participate.Participant', to=settings.AUTH_USER_MODEL, verbose_name='Users'),
        ),
        migrations.AddField(
            model_name='questionpaper',
            name='questions',
            field=models.ManyToManyField(related_name='includes', to='question.Question', verbose_name='Questions'),
        ),
        migrations.AddField(
            model_name='answerpaper',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='answerpapers', to='participate.Participant'),
        ),
        migrations.AddField(
            model_name='answerpaper',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='answerpapers', to='quiz.Quiz'),
        ),
        migrations.AddField(
            model_name='answer',
            name='answerpaper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='answers', to='quiz.AnswerPaper', verbose_name='AnswerPaper'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='question.Question'),
        ),
    ]