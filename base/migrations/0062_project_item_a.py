# Generated by Django 3.2.14 on 2022-08-11 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0061_itema'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='item_a',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.itema'),
        ),
    ]
