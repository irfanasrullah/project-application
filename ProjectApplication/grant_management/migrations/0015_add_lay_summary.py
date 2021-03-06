# Generated by Django 3.0.5 on 2020-04-28 08:54

from django.db import migrations, models
import django.db.models.deletion

def add_default_lay_summary_type(apps, schema_editor):
    LaySummaryType = apps.get_model('grant_management', 'LaySummaryType')
    LaySummaryType.objects.get_or_create(name='Internal', defaults={'description': 'Used internally by SPI'})
    LaySummaryType.objects.get_or_create(name='Web', defaults={'description': 'To be published to the web'})

class Migration(migrations.Migration):

    dependencies = [
        ('grant_management', '0014_financial_report_rename_signed_to_approved_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='LaySummaryType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, help_text='Date and time at which the entry was created')),
                ('modified_on', models.DateTimeField(auto_now=True, help_text='Date and time at which the entry was modified', null=True)),
                ('name', models.CharField(max_length=10, unique=True)),
                ('description', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='laysummary',
            name='web_version',
        ),
        migrations.RunPython(add_default_lay_summary_type),
        migrations.AddField(
            model_name='laysummary',
            name='lay_summary_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='grant_management.LaySummaryType'),
            preserve_default=False,
        ),
    ]
