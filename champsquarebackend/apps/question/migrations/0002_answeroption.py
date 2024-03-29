# Generated by Django 3.0.5 on 2020-11-27 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='If option has any images')),
                ('correct', models.BooleanField(default=False, verbose_name='Whether this option is correct or not')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_options', to='question.Question')),
            ],
            options={
                'verbose_name': 'AnswerOption',
                'verbose_name_plural': 'AnswerOptions',
                'ordering': ['id'],
                'abstract': False,
            },
        ),
    ]
