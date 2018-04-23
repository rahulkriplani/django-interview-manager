# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-23 13:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Evaluator', '0010_interview_exam'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='QuestionSet', max_length=200)),
                ('times_taken', models.IntegerField(default=0, editable=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='interview',
            name='exam',
        ),
        migrations.RemoveField(
            model_name='question',
            name='exam',
        ),
        migrations.DeleteModel(
            name='Exam',
        ),
        migrations.AddField(
            model_name='interview',
            name='question_set',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Evaluator.QuestionSet'),
        ),
        migrations.AddField(
            model_name='question',
            name='qset',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Evaluator.QuestionSet'),
        ),
    ]
