# Generated by Django 3.0.3 on 2020-04-08 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grant_management', '0005_grant_agreement_one_to_one'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financereport',
            name='reception_date',
            field=models.DateField(blank=True, help_text='Date that the document was received', null=True),
        ),
        migrations.AlterField(
            model_name='financereport',
            name='sent_date',
            field=models.DateField(blank=True, help_text='Date that the document was sent', null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='reception_date',
            field=models.DateField(blank=True, help_text='Date that the document was received', null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='sent_date',
            field=models.DateField(blank=True, help_text='Date that the document was sent', null=True),
        ),
        migrations.AlterField(
            model_name='laysummary',
            name='reception_date',
            field=models.DateField(blank=True, help_text='Date that the document was received', null=True),
        ),
        migrations.AlterField(
            model_name='laysummary',
            name='sent_date',
            field=models.DateField(blank=True, help_text='Date that the document was sent', null=True),
        ),
        migrations.AlterField(
            model_name='media',
            name='reception_date',
            field=models.DateField(blank=True, help_text='Date that the document was received', null=True),
        ),
        migrations.AlterField(
            model_name='media',
            name='sent_date',
            field=models.DateField(blank=True, help_text='Date that the document was sent', null=True),
        ),
    ]
