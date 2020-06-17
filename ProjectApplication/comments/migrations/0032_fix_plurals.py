# Generated by Django 3.0.5 on 2020-06-02 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0031_grantagreementattachment_grantagreementattachmentcategory_grantagreementcomment_grantagreementcommen'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grantagreementattachment',
            options={'verbose_name_plural': 'Grant Agreement Attachments'},
        ),
        migrations.AlterModelOptions(
            name='grantagreementcomment',
            options={'verbose_name_plural': 'Grant Agreement Comments'},
        ),
        migrations.AlterModelOptions(
            name='grantagreementcommentcategory',
            options={'verbose_name_plural': 'Grant Agreement Comment Categories'},
        ),
        migrations.AlterUniqueTogether(
            name='grantagreementattachment',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='grantagreementcomment',
            unique_together=set(),
        ),
    ]