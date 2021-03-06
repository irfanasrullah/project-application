# Generated by Django 3.0.3 on 2020-03-24 15:18

import django.core.validators
from django.db import migrations, models
import project_core.utils.orcid


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0113_changes_orcid_field_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalphysicalperson',
            name='orcid',
            field=models.CharField(db_index=True, help_text='Orcid ID', max_length=19, null=True, validators=[project_core.utils.orcid.raise_error_if_orcid_invalid, django.core.validators.RegexValidator(code='Invalid format', message='Invalid format for ORCID iD. E.g.: 0000-0002-1825-0097.', regex='^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[0-9X]$')]),
        ),
        migrations.AlterField(
            model_name='physicalperson',
            name='orcid',
            field=models.CharField(help_text='Orcid ID', max_length=19, null=True, unique=True, validators=[project_core.utils.orcid.raise_error_if_orcid_invalid, django.core.validators.RegexValidator(code='Invalid format', message='Invalid format for ORCID iD. E.g.: 0000-0002-1825-0097.', regex='^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[0-9X]$')]),
        ),
        migrations.AlterUniqueTogether(
            name='physicalperson',
            unique_together=set(),
        ),
    ]
