# Generated by Django 3.0.7 on 2020-06-15 14:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project_core', '0125_from_latin1_to_utf8bm4'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproject',
            name='closed_by',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalproject',
            name='closed_on',
            field=models.DateTimeField(help_text='When the project was closed', null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='closed_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='closed_on',
            field=models.DateTimeField(help_text='When the project was closed', null=True),
        ),
    ]