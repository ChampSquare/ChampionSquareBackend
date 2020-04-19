# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-14 13:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Uscholar', '0002_auto_20181213_1927'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_attempt', models.IntegerField(default=0)),
                ('num_correct', models.IntegerField(default=0)),
                ('num_wrong', models.IntegerField(default=0)),
                ('marks_obtained', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_num', models.IntegerField(default=0)),
                ('user_answer', models.CharField(max_length=5)),
                ('right_answer', models.CharField(max_length=5)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Uscholar.Question')),
            ],
        ),
        migrations.AddField(
            model_name='result',
            name='answer',
            field=models.ManyToManyField(to='JeeMain.UserAnswer'),
        ),
        migrations.AddField(
            model_name='result',
            name='question_paper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Uscholar.QuestionPaper'),
        ),
        migrations.AddField(
            model_name='result',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
