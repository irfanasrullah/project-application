# Generated by Django 2.2.6 on 2019-10-28 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0071_rename_callquestion_question_to_template_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='call',
            name='other_funding_question',
            field=models.BooleanField(blank=True, help_text='True if the Other Funding question is enabled', null=True),
        ),
    ]