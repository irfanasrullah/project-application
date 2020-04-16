# Generated by Django 3.0.3 on 2020-04-07 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0118_calls_need_to_be_part_of_a_funding_instrument'),
        ('grant_management', '0004_minor_changes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grantagreement',
            name='project',
            field=models.OneToOneField(help_text='Project that this Grant Agreement belongs to', on_delete=django.db.models.deletion.PROTECT, to='project_core.Project'),
        ),
    ]