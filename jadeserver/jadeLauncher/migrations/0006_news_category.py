# Generated by Django 4.1.2 on 2022-11-01 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jadeLauncher', '0005_alter_news_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='category',
            field=models.CharField(default='', max_length=100),
        ),
    ]
