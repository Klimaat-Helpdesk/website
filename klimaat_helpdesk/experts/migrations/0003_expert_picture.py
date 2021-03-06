# Generated by Django 2.2.9 on 2020-01-12 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0001_squashed_0021'),
        ('experts', '0002_remove_expert_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='expert',
            name='picture',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
    ]
