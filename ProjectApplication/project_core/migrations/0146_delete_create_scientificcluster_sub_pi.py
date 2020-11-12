# Generated by Django 3.0.10 on 2020-11-12 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0145_auto_rename_scientific_cluster_to_clusters'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposalscientificcluster',
            name='applicant',
        ),
        migrations.AddField(
            model_name='proposalscientificcluster',
            name='sub_pi',
            field=models.ForeignKey(default=None, help_text='Main person of this scientific cluster', on_delete=django.db.models.deletion.PROTECT, to='project_core.PersonPosition'),
            preserve_default=False,
        ),
    ]
