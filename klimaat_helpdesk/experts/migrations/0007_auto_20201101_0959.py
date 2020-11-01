# Generated by Django 3.1.2 on 2020-11-01 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experts', '0006_auto_20201024_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expert',
            name='linkedin_profile',
            field=models.URLField(blank=True, null=True, verbose_name='LinkedIn Profile'),
        ),
        migrations.AlterField(
            model_name='expert',
            name='twitter_profile',
            field=models.URLField(blank=True, null=True, verbose_name='Twitter Profile'),
        ),
    ]
