# Generated by Django 2.2.6 on 2019-10-23 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0067_proposal_duration_minvalue'),
    ]

    operations = [
        migrations.AddField(
            model_name='personposition',
            name='contact_newsletter',
            field=models.BooleanField(default=False, help_text='Agree or disagree to being contacted by email with newsletter'),
        ),
        migrations.AddField(
            model_name='personposition',
            name='data_policy',
            field=models.BooleanField(default=False, help_text='Agree or disagree to the data policy for storage of personal information'),
        ),
    ]