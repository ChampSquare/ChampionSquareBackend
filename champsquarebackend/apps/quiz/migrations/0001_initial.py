# Generated by Django 2.2 on 2020-07-21 06:25

import champsquarebackend.models.fields.autoslugfield
import ckeditor_uploader.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True, verbose_name='used to store metadata')),
                ('answer', models.CharField(blank=True, max_length=128, verbose_name='Answer')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Is this answer correct?')),
                ('points', models.FloatField(default=0.0, verbose_name='points gained')),
                ('status', models.CharField(choices=[('unvisited', 'Not Visited'), ('unanswered', 'Unanswered'), ('answered', 'Answered'), ('marked', 'Marked For Review'), ('answered_marked', 'Answered & Marked For Review')], default='unvisited', max_length=30, verbose_name='Status of Answer')),
                ('time_taken', models.FloatField(default=0.0, help_text='Time Spent on particular question', verbose_name='Time Taken')),
            ],
            options={
                'verbose_name': 'Answer submitted by user',
                'verbose_name_plural': 'Answers submitted by user',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AnswerPaper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True, verbose_name='used to store metadata')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='datetime when model is created')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='datetime when model is updated last time')),
                ('participant_number', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('is_trial', models.BooleanField(default=False, verbose_name='Is trial?')),
                ('last_accessed', models.DateTimeField(blank=True, null=True, verbose_name='Last Access Time')),
                ('is_started', models.BooleanField(default=False, verbose_name='Is test started?')),
                ('is_submitted', models.BooleanField(default=False, verbose_name='Is Test Submitted?')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='Start time of paper')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='End time of paper')),
            ],
            options={
                'verbose_name': 'AnswerPaper',
                'verbose_name_plural': 'AnswerPapers',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=128, unique=True, verbose_name='Name')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Description')),
                ('image', models.ImageField(blank=True, null=True, upload_to='categories', verbose_name='Image')),
                ('slug', champsquarebackend.models.fields.autoslugfield.AutoSlugField(blank=True, editable=False, max_length=128, populate_from='name', unique=True, verbose_name='Slug')),
                ('is_public', models.BooleanField(db_index=True, default=False, verbose_name='Is Public')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QuestionPaper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True, verbose_name='used to store metadata')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='datetime when model is created')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='datetime when model is updated last time')),
                ('shuffle_questions', models.BooleanField(default=False)),
                ('total_questions', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'QuestionPaper',
                'verbose_name_plural': 'QuestionPapers',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True, verbose_name='used to store metadata')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='datetime when model is created')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='datetime when model is updated last time')),
                ('name', models.CharField(help_text='Name of quiz', max_length=128, verbose_name='name')),
                ('slug', champsquarebackend.models.fields.autoslugfield.AutoSlugField(blank=True, editable=False, max_length=128, populate_from='name', unique=True, verbose_name='slug')),
                ('start_date_time', models.DateTimeField(default=django.utils.timezone.now, help_text='Date-time from which this quiz will be active', verbose_name='Start date-time of quiz')),
                ('end_date_time', models.DateTimeField(blank=True, help_text='Date-time after which this quiz will be deactivated automatically', null=True, verbose_name='End date-time of quiz')),
                ('duration', models.PositiveIntegerField(default=60, help_text='Duration of quiz in minutes', verbose_name='Duration of quiz')),
                ('total_marks', models.FloatField(default=0.0)),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('instructions', ckeditor_uploader.fields.RichTextUploadingField(blank=True, help_text='Instructions to show users before they take exam', null=True, verbose_name='instructions of quiz')),
                ('is_published', models.BooleanField(default=False, help_text="Publish the quiz, won't be accessible if you don't publish it", verbose_name='Publish')),
                ('is_public', models.BooleanField(default=False, help_text='Public quizzes will appear in quiz catalogue and can be taken by users registered on site', verbose_name='Public')),
                ('multiple_attempts_allowed', models.BooleanField(default=False, help_text='Is user allowed to attempt same quiz multiple time?')),
                ('view_answerpaper', models.BooleanField(default=False, help_text='Is user allowed to view his test report after he submits the test!')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quiz_category', to='quiz.Category')),
                ('questionpaper', models.OneToOneField(blank=True, help_text='Questionpaper which will be given to user taking this quiz', null=True, on_delete=django.db.models.deletion.PROTECT, to='quiz.QuestionPaper', verbose_name='questionpaper')),
            ],
            options={
                'verbose_name': 'Quiz',
                'verbose_name_plural': 'Quizzes',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
    ]
