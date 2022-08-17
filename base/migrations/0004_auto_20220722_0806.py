# Generated by Django 3.1.7 on 2022-07-22 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_responsible_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='projectName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='project',
            name='name',
        ),
        migrations.AddField(
            model_name='project',
            name='p_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.projectname'),
        ),
        migrations.AddField(
            model_name='responsible',
            name='p_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.projectname'),
        ),
    ]