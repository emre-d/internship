# Generated by Django 3.2.14 on 2022-08-11 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0058_alter_project_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='oldStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_status', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='project',
            name='item',
        ),
    ]
