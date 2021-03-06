# Generated by Django 3.0.8 on 2020-07-30 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_core', '0130_postaladdress'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproposal',
            name='postal_address',
            field=models.ForeignKey(blank=True, db_constraint=False, help_text='Address to where the grant agreement is going to be sent', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='project_core.PostalAddress'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='postal_address',
            field=models.ForeignKey(help_text='Address to where the grant agreement is going to be sent', null=True, on_delete=django.db.models.deletion.PROTECT, to='project_core.PostalAddress'),
        ),
        migrations.AlterField(
            model_name='postaladdress',
            name='address',
            field=models.TextField(help_text='Include street/avenue, block, building, floor, door, etc.'),
        ),
    ]
