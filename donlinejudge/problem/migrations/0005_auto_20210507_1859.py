# Generated by Django 3.1 on 2021-05-07 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0004_auto_20210507_1855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='memory_limit',
            field=models.IntegerField(default=256),
        ),
        migrations.AlterField(
            model_name='problem',
            name='time_limit',
            field=models.IntegerField(default=1000),
        ),
    ]
