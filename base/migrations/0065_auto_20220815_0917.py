# Generated by Django 3.2.14 on 2022-08-15 06:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0064_auto_20220815_0913'),
    ]

    operations = [
        migrations.CreateModel(
            name='impCoff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imp', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='project',
            name='item_a',
        ),
        migrations.CreateModel(
            name='impTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('implemTime', models.CharField(blank=True, max_length=200, null=True)),
                ('impcoff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.impcoff')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='impVar',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.imptime'),
        ),
    ]