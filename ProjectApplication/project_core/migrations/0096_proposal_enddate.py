# Generated by Django 2.2.6 on 2019-12-04 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0095_proposal_startdate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proposal',
            old_name='provisional_end_date',
            new_name='end_date',
        ),
    ]