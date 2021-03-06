# Generated by Django 3.0.5 on 2020-04-19 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_question_asked_by_ip'),
    ]

    operations = [
        migrations.CreateModel(
            name='GitlabIssues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_id', models.IntegerField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('question', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='issue', to='core.Question')),
            ],
        ),
    ]
