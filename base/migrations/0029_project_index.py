# Generated by Django 3.2.14 on 2022-08-02 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0028_delete_digi'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='index',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]