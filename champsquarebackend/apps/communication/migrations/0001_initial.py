# Generated by Django 2.2 on 2020-07-26 05:50

import champsquarebackend.models.fields.autoslugfield
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommunicationEventType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='datetime when model is created')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='datetime when model is updated last time')),
                ('code', champsquarebackend.models.fields.autoslugfield.AutoSlugField(blank=True, editable=False, help_text='Code used for looking up this event programmatically', max_length=128, populate_from='name', separator='_', unique=True, validators=[django.core.validators.RegexValidator(message="Code can only contain the uppercase letters (A-Z), digits, and underscores, and can't start with a digit.", regex='^[A-Z_][0-9A-Z_]*$')], verbose_name='Code')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('category', models.CharField(choices=[('Quiz related', 'Quiz related'), ('User related', 'User related')], default='Quiz related', max_length=255, verbose_name='Category')),
                ('email_subject_template', models.CharField(blank=True, max_length=255, null=True, verbose_name='Email Subject Template')),
                ('email_body_template', models.TextField(blank=True, null=True, verbose_name='Email Body Template')),
                ('email_body_html_template', models.TextField(blank=True, help_text='HTML template', null=True, verbose_name='Email Body HTML Template')),
                ('sms_template', models.CharField(blank=True, help_text='SMS template', max_length=170, null=True, verbose_name='SMS Template')),
            ],
            options={
                'verbose_name': 'Communication event type',
                'verbose_name_plural': 'Communication event types',
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='datetime when model is created')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='datetime when model is updated last time')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email Address')),
                ('subject', models.TextField(max_length=255, verbose_name='Subject')),
                ('body_text', models.TextField(verbose_name='Body Text')),
                ('body_html', models.TextField(blank=True, verbose_name='Body HTML')),
                ('date_sent', models.DateTimeField(auto_now_add=True, verbose_name='Date Sent')),
            ],
            options={
                'verbose_name': 'Email',
                'verbose_name_plural': 'Emails',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='datetime when model is created')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='datetime when model is updated last time')),
                ('subject', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('location', models.CharField(choices=[('Inbox', 'Inbox'), ('Archive', 'Archive')], default='Inbox', max_length=32)),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
                ('date_read', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
                'ordering': ('-date_sent',),
            },
        ),
    ]
