# Generated by Django 3.0.5 on 2020-08-10 07:48

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0014_auto_20200810_0746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expertindexpage',
            name='intro',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
        migrations.AlterField(
            model_name='expertindexpage',
            name='outro',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
    ]
