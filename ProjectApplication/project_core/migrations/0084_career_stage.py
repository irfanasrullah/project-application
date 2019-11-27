# Generated by Django 2.2.6 on 2019-11-27 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0083_call_project_overarching_question'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposalpartner',
            name='career_stage',
        ),
        migrations.AddField(
            model_name='personposition',
            name='career_stage',
            field=models.ForeignKey(default='', help_text='Stage of the person in the career', on_delete=django.db.models.deletion.PROTECT, to='project_core.CareerStage'),
            preserve_default=False,
        ),
    ]
