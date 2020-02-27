# Generated by Django 3.0.3 on 2020-02-27 14:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('colours', '0002_renames_colorpair_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='colour',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='Date and time at which the entry was created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='colour',
            name='modified_on',
            field=models.DateTimeField(auto_now=True, help_text='Date and time at which the entry was modified', null=True),
        ),
        migrations.AddField(
            model_name='colourpair',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='Date and time at which the entry was created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='colourpair',
            name='modified_on',
            field=models.DateTimeField(auto_now=True, help_text='Date and time at which the entry was modified', null=True),
        ),
    ]