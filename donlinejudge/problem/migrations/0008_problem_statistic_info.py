# Generated by Django 3.1 on 2021-05-07 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0007_remove_problem_statistic_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='statistic_info',
            field=models.JSONField(default=dict),
        ),
    ]
