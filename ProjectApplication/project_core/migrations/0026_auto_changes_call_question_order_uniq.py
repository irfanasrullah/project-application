# Generated by Django 2.2.6 on 2019-10-08 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0025_delete_message_unique_constraints'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callquestion',
            name='order',
            field=models.PositiveIntegerField(help_text='Use the integer order to order the questions'),
        ),
        migrations.AlterUniqueTogether(
            name='callquestion',
            unique_together={('call', 'order'), ('call', 'question')},
        ),
    ]