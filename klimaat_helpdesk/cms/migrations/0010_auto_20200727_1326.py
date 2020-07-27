# Generated by Django 3.0.5 on 2020-07-27 13:26

from django.db import migrations
import klimaat_helpdesk.cms.blocks
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0009_answer_introduction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='content',
        ),
        migrations.AddField(
            model_name='answer',
            name='answer_origin',
            field=wagtail.core.fields.StreamField([('origin', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(max_length=255)), ('content', wagtail.core.blocks.RichTextBlock()), ('sources', wagtail.core.blocks.ListBlock(klimaat_helpdesk.cms.blocks.ScientificSourceBlock))]))], default=None),
            preserve_default=False,
        ),
    ]
