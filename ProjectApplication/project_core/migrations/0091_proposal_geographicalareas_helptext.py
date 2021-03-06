# Generated by Django 2.2.6 on 2019-12-03 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0090_proposal_duration_helptext'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='location',
            field=models.CharField(blank=True, help_text='Name of more precise location of where proposal would take place (not coordinates)', max_length=200, null=True),
        ),
    ]
