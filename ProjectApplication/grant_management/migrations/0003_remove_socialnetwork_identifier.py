# Generated by Django 3.0.3 on 2020-04-06 07:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grant_management', '0002_socialnetwork_identifier'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socialnetwork',
            name='identifier',
        ),
    ]
