# Generated by Django 3.2.5 on 2021-08-07 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('judgeserver', '0003_auto_20210519_2054'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='judgeserver',
            options={'ordering': ['-id', '-is_disabled']},
        ),
    ]
