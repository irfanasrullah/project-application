# Generated by Django 3.0.3 on 2020-02-27 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('variable_templates', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='callvariabletemplate',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='callvariabletemplate',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='fundinginstrumentvariabletemplate',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='fundinginstrumentvariabletemplate',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='templatevariablename',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='templatevariablename',
            name='modified_by',
        ),
    ]