# Generated by Django 3.2.14 on 2022-08-01 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_project_perc'),
    ]

    operations = [
        migrations.CreateModel(
            name='Percentage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zorluk', models.IntegerField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='project',
            name='perc',
        ),
    ]