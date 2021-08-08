# Generated by Django 3.1 on 2021-05-09 09:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProblemTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagName', models.TextField()),
            ],
            options={
                'db_table': 'problemtag',
            },
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_id', models.TextField(db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('visible', models.BooleanField(default=True)),
                ('title', models.TextField()),
                ('statement', models.TextField()),
                ('difficulty', models.CharField(choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], default='Easy', max_length=50)),
                ('source', models.TextField(null=True)),
                ('sample_test', models.JSONField(default=dict, null=True)),
                ('testset_dir', models.TextField(null=True)),
                ('testset_count', models.PositiveIntegerField(default=0)),
                ('time_limit', models.IntegerField(default=1000)),
                ('memory_limit', models.IntegerField(default=256)),
                ('total_submission', models.BigIntegerField(default=0)),
                ('correct_submission', models.BigIntegerField(default=0)),
                ('statistic_info', models.JSONField(default=dict)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(to='problem.ProblemTag')),
            ],
            options={
                'db_table': 'problem',
                'ordering': ['created'],
            },
        ),
    ]
