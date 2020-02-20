# Generated by Django 3.0.3 on 2020-02-19 12:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0104_delete_colour'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('evaluation', '0004_create_proposal_evaluation'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposalevaluation',
            name='created_by',
            field=models.ForeignKey(blank=True, help_text='User by which the entry was created', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='evaluation_proposalevaluation_created_by_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='proposalevaluation',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='Date and time at which the entry was created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proposalevaluation',
            name='modified_by',
            field=models.ForeignKey(blank=True, help_text='User by which the entry was modified', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='evaluation_proposalevaluation_modified_by_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='proposalevaluation',
            name='modified_on',
            field=models.DateTimeField(auto_now=True, help_text='Date and time at which the entry was modified', null=True),
        ),
        migrations.AlterField(
            model_name='proposalevaluation',
            name='board_decision',
            field=models.CharField(choices=[('Fund', 'Fund'), ('NotFund', 'Not Fund')], max_length=7),
        ),
        migrations.CreateModel(
            name='CallEvaluation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, help_text='Date and time at which the entry was created')),
                ('modified_on', models.DateTimeField(auto_now=True, help_text='Date and time at which the entry was modified', null=True)),
                ('panel_date', models.DateField()),
                ('call', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='project_core.Call')),
                ('created_by', models.ForeignKey(blank=True, help_text='User by which the entry was created', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='evaluation_callevaluation_created_by_related', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, help_text='User by which the entry was modified', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='evaluation_callevaluation_modified_by_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]