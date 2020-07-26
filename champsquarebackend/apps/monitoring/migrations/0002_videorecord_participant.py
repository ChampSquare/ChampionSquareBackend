# Generated by Django 2.2 on 2020-07-26 05:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('participate', '0001_initial'),
        ('monitoring', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='videorecord',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='videos', to='participate.Participant', verbose_name='Participant'),
        ),
    ]