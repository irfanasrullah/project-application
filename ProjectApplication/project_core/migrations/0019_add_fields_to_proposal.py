# Generated by Django 2.2.6 on 2019-10-07 11:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0018_callquestion_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='date_started',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Date and time (UTC) at which the proposal was first started'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='last_modified',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Latest date and time at which the proposal was modified'),
        ),
    ]
