# Generated by Django 3.0.3 on 2020-03-23 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0112_physical_person_add_orcid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalphysicalperson',
            old_name='orcid_id',
            new_name='orcid',
        ),
        migrations.RenameField(
            model_name='physicalperson',
            old_name='orcid_id',
            new_name='orcid',
        ),
    ]