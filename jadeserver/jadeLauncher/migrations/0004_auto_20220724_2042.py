# Generated by Django 3.2.3 on 2022-07-24 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jadeLauncher', '0003_alter_newscodes_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='version',
            name='major',
            field=models.CharField(default='0', max_length=3),
        ),
        migrations.AlterField(
            model_name='version',
            name='minor',
            field=models.CharField(default='0', max_length=3),
        ),
        migrations.AlterField(
            model_name='version',
            name='patch',
            field=models.CharField(default='0', max_length=3),
        ),
    ]
