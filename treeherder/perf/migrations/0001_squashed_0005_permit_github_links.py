# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-08 13:19
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('model', '0001_squashed_0022_modify_bugscache_and_bugjobmap'),
    ]

    operations = [
        migrations.CreateModel(
            name='IssueTracker',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('task_base_url', models.URLField(max_length=512)),
            ],
            options={
                'db_table': 'issue_tracker',
            },
        ),
        migrations.CreateModel(
            name='PerformanceFramework',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                ('name', models.SlugField(max_length=255, unique=True)),
                ('enabled', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'performance_framework',
            },
        ),
        migrations.CreateModel(
            name='PerformanceBugTemplate',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                ('keywords', models.CharField(max_length=255)),
                ('status_whiteboard', models.CharField(max_length=255)),
                ('default_component', models.CharField(max_length=255)),
                ('default_product', models.CharField(max_length=255)),
                ('cc_list', models.CharField(max_length=255)),
                ('text', models.TextField(max_length=4096)),
                (
                    'framework',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to='perf.PerformanceFramework'
                    ),
                ),
            ],
            options={
                'db_table': 'performance_bug_template',
            },
        ),
        migrations.CreateModel(
            name='PerformanceSignature',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                (
                    'signature_hash',
                    models.CharField(
                        max_length=40, validators=[django.core.validators.MinLengthValidator(40)]
                    ),
                ),
                ('suite', models.CharField(max_length=80)),
                ('test', models.CharField(blank=True, max_length=80)),
                ('lower_is_better', models.BooleanField(default=True)),
                ('last_updated', models.DateTimeField(db_index=True)),
                ('has_subtests', models.BooleanField()),
                ('extra_options', models.CharField(blank=True, max_length=60)),
                ('should_alert', models.NullBooleanField()),
                (
                    'alert_change_type',
                    models.IntegerField(choices=[(0, 'percentage'), (1, 'absolute')], null=True),
                ),
                ('alert_threshold', models.FloatField(null=True)),
                ('min_back_window', models.IntegerField(null=True)),
                ('max_back_window', models.IntegerField(null=True)),
                ('fore_window', models.IntegerField(null=True)),
                (
                    'framework',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='perf.PerformanceFramework'
                    ),
                ),
                (
                    'option_collection',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='model.OptionCollection'
                    ),
                ),
                (
                    'parent_signature',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='subtests',
                        to='perf.PerformanceSignature',
                    ),
                ),
                (
                    'platform',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='model.MachinePlatform'
                    ),
                ),
                (
                    'repository',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='model.Repository'
                    ),
                ),
            ],
            options={
                'db_table': 'performance_signature',
            },
        ),
        migrations.CreateModel(
            name='PerformanceDatum',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                ('value', models.FloatField()),
                ('push_timestamp', models.DateTimeField()),
                ('ds_job_id', models.PositiveIntegerField(db_column='ds_job_id', null=True)),
                ('result_set_id', models.PositiveIntegerField(null=True)),
                (
                    'job',
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to='model.Job',
                    ),
                ),
                (
                    'push',
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.Push'),
                ),
                (
                    'repository',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='model.Repository'
                    ),
                ),
                (
                    'signature',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='perf.PerformanceSignature'
                    ),
                ),
            ],
            options={
                'db_table': 'performance_datum',
            },
        ),
        migrations.CreateModel(
            name='PerformanceAlertSummary',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('manually_created', models.BooleanField(default=False)),
                ('last_updated', models.DateTimeField(db_index=True)),
                (
                    'status',
                    models.IntegerField(
                        choices=[
                            (0, 'Untriaged'),
                            (1, 'Downstream'),
                            (3, 'Invalid'),
                            (4, 'Improvement'),
                            (5, 'Investigating'),
                            (6, "Won't fix"),
                            (7, 'Fixed'),
                            (8, 'Backed out'),
                        ],
                        default=0,
                    ),
                ),
                ('bug_number', models.PositiveIntegerField(null=True)),
                (
                    'framework',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='perf.PerformanceFramework'
                    ),
                ),
                (
                    'prev_push',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='+',
                        to='model.Push',
                    ),
                ),
                (
                    'push',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='+',
                        to='model.Push',
                    ),
                ),
                (
                    'repository',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='model.Repository'
                    ),
                ),
                (
                    'issue_tracker',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to='perf.IssueTracker',
                    ),
                ),
            ],
            options={
                'db_table': 'performance_alert_summary',
            },
        ),
        migrations.CreateModel(
            name='PerformanceAlert',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_regression', models.BooleanField()),
                (
                    'status',
                    models.IntegerField(
                        choices=[
                            (0, 'Untriaged'),
                            (1, 'Downstream'),
                            (2, 'Reassigned'),
                            (3, 'Invalid'),
                            (4, 'Acknowledged'),
                        ],
                        default=0,
                    ),
                ),
                (
                    'amount_pct',
                    models.FloatField(help_text='Amount in percentage that series has changed'),
                ),
                (
                    'amount_abs',
                    models.FloatField(help_text='Absolute amount that series has changed'),
                ),
                (
                    'prev_value',
                    models.FloatField(help_text='Previous value of series before change'),
                ),
                ('new_value', models.FloatField(help_text='New value of series after change')),
                (
                    't_value',
                    models.FloatField(
                        help_text="t value out of analysis indicating confidence that change is 'real'",
                        null=True,
                    ),
                ),
                ('manually_created', models.BooleanField(default=False)),
                (
                    'classifier',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'related_summary',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='related_alerts',
                        to='perf.PerformanceAlertSummary',
                    ),
                ),
                (
                    'series_signature',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='perf.PerformanceSignature'
                    ),
                ),
                (
                    'summary',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='alerts',
                        to='perf.PerformanceAlertSummary',
                    ),
                ),
            ],
            options={
                'db_table': 'performance_alert',
            },
        ),
        migrations.AlterUniqueTogether(
            name='performancesignature',
            unique_together=set([('repository', 'framework', 'signature_hash')]),
        ),
        migrations.AlterUniqueTogether(
            name='performancedatum',
            unique_together=set([('repository', 'job', 'push', 'signature')]),
        ),
        migrations.AlterIndexTogether(
            name='performancedatum',
            index_together=set(
                [('repository', 'signature', 'push_timestamp'), ('repository', 'signature', 'push')]
            ),
        ),
        migrations.AlterUniqueTogether(
            name='performancealertsummary',
            unique_together=set([('repository', 'framework', 'prev_push', 'push')]),
        ),
        migrations.AlterUniqueTogether(
            name='performancealert',
            unique_together=set([('summary', 'series_signature')]),
        ),
    ]
