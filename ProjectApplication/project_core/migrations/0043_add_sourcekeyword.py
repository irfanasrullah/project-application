# Generated by Django 2.2.6 on 2019-10-22 08:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project_core', '0042_createmodify_source'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeywordSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, help_text='Date and time at which the entry was created')),
                ('modified_on', models.DateTimeField(blank=True, help_text='Date and time at which the entry was modified', null=True)),
                ('uuid', models.UUIDField(db_index=True, unique=True)),
                ('created_by', models.ForeignKey(blank=True, help_text='User by which the entry was created', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='project_core_keywordsource_created_by_related', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, help_text='User by which the entry was modified', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='project_core_keywordsource_modified_by_related', to=settings.AUTH_USER_MODEL)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='project_core.Source')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='keyword',
            name='source',
            field=models.ForeignKey(help_text='Source from which the keyword originated', on_delete=django.db.models.deletion.PROTECT, to='project_core.KeywordSource'),
        ),
    ]
