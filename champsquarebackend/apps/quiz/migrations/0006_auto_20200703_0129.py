# Generated by Django 2.2 on 2020-07-02 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_auto_20200703_0101'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answerpaper',
            options={'verbose_name': 'AnswerPaper', 'verbose_name_plural': 'AnswerPapers'},
        ),
        migrations.AlterModelOptions(
            name='questionpaper',
            options={'verbose_name': 'QuestionPaper', 'verbose_name_plural': 'QuestionPapers'},
        ),
        migrations.AlterModelOptions(
            name='quiz',
            options={'ordering': ['name'], 'verbose_name': 'Quiz', 'verbose_name_plural': 'Quizzes'},
        ),
        migrations.AlterField(
            model_name='quiz',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quiz_category', to='quiz.Category'),
        ),
    ]
