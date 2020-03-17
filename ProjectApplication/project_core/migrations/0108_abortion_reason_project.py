# Generated by Django 3.0.3 on 2020-03-16 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0107_project_allocated_budget'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='abortion_reason',
            field=models.CharField(blank=True, help_text='Reason that a project was aborted', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('Ongoing', 'Ongoing'), ('Completed', 'Completed'), ('Aborted', 'Aborted')], default='ONGOING', help_text='Status of a project', max_length=30),
        ),
    ]