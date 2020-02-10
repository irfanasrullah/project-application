# Generated by Django 2.2.6 on 2020-02-10 11:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project_core', '0101_auto_20200207_1144'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, help_text='Date and time at which the entry was created')),
                ('modified_on', models.DateTimeField(auto_now=True, help_text='Date and time at which the entry was modified', null=True)),
                ('category', models.CharField(help_text='Type of comment or attachment', max_length=100, unique=True)),
                ('created_by', models.ForeignKey(blank=True, help_text='User by which the entry was created', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='comments_category_created_by_related', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, help_text='User by which the entry was modified', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='comments_category_modified_by_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='ProposalCommentCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, help_text='Date and time at which the entry was created')),
                ('modified_on', models.DateTimeField(auto_now=True, help_text='Date and time at which the entry was modified', null=True)),
                ('comment_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='comments.Category')),
                ('created_by', models.ForeignKey(blank=True, help_text='User by which the entry was created', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='comments_proposalcommentcategory_created_by_related', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, help_text='User by which the entry was modified', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='comments_proposalcommentcategory_modified_by_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Proposal Comment Categories',
            },
        ),
        migrations.CreateModel(
            name='ProposalComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, help_text='Date and time at which the entry was created')),
                ('modified_on', models.DateTimeField(auto_now=True, help_text='Date and time at which the entry was modified', null=True)),
                ('text', models.TextField(help_text='Comment text')),
                ('comment_category', models.ForeignKey(help_text='Type of comment', on_delete=django.db.models.deletion.PROTECT, to='comments.ProposalCommentCategory')),
                ('created_by', models.ForeignKey(blank=True, help_text='User by which the entry was created', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='comments_proposalcomment_created_by_related', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, help_text='User by which the entry was modified', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='comments_proposalcomment_modified_by_related', to=settings.AUTH_USER_MODEL)),
                ('proposal', models.ForeignKey(help_text='Proposal that this comment refers to', on_delete=django.db.models.deletion.PROTECT, to='project_core.Proposal')),
            ],
            options={
                'unique_together': {('proposal', 'created_on', 'created_by')},
            },
        ),
        migrations.CreateModel(
            name='CallComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, help_text='Date and time at which the entry was created')),
                ('modified_on', models.DateTimeField(auto_now=True, help_text='Date and time at which the entry was modified', null=True)),
                ('text', models.TextField(help_text='Comment text')),
                ('call', models.ForeignKey(help_text='Call about which the comment was made', on_delete=django.db.models.deletion.PROTECT, to='project_core.Call')),
                ('created_by', models.ForeignKey(blank=True, help_text='User by which the entry was created', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='comments_callcomment_created_by_related', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, help_text='User by which the entry was modified', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='comments_callcomment_modified_by_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('call', 'created_on', 'created_by')},
            },
        ),
    ]
