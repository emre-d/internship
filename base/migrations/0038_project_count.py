# Generated by Django 3.2.14 on 2022-08-04 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0037_alter_function_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
