# Generated by Django 3.1.7 on 2021-11-08 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0003_topic_is_superadmin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='is_superadmin',
        ),
    ]
