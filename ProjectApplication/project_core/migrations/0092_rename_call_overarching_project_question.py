# Generated by Django 2.2.6 on 2019-12-03 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0091_proposal_geographicalareas_helptext'),
    ]

    operations = [
        migrations.RenameField(
            model_name='call',
            old_name='project_overarching_question',
            new_name='overarching_project_question',
        ),
    ]
