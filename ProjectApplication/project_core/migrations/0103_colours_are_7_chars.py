# Generated by Django 2.2.6 on 2020-02-12 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0102_colour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colour',
            name='hex_code',
            field=models.CharField(help_text='Hex code, e.g. FF0000 for red', max_length=7, unique=True),
        ),
    ]
