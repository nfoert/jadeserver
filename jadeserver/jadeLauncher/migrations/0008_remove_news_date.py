# Generated by Django 4.1.2 on 2022-11-01 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jadeLauncher', '0007_alter_news_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='date',
        ),
    ]
