# Generated by Django 3.2.14 on 2022-08-15 06:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0063_auto_20220815_0850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imptime',
            name='imp',
        ),
        migrations.RemoveField(
            model_name='project',
            name='implem',
        ),
        migrations.DeleteModel(
            name='impCof',
        ),
        migrations.DeleteModel(
            name='impTime',
        ),
    ]