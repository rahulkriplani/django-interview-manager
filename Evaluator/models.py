# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator
from django.shortcuts import redirect
from datetime import datetime

class Position(models.Model):
    name = models.CharField(max_length=50)
    id_code = models.CharField(max_length=10)
    exp_needed = models.PositiveIntegerField(default=0)
    technology = models.TextField(default='')
    location = models.CharField(max_length=100, default='Pune')
    type_choices = (
        ('P', 'Permanent'),
        ('T', 'Temporary'),
        ('I', 'Intern'),
                     )
    j_type = models.CharField( # This field can be shown in template as get_status_display
                        max_length=1,
                        choices=type_choices,
                        default='P'
                             )

    def __str__(self):  # __unicode__ on Python 2
        return self.name

class Candidate(models.Model):
    name = models.CharField(max_length=40)
    contact_validator = RegexValidator(regex='\d+')
    contact_primary = models.CharField(max_length=20, validators=[contact_validator], null=True)
    experience = models.PositiveIntegerField()
    position_applied = models.ForeignKey(Position)


    def __str__(self):  # __unicode__ on Python 2
        return self.name

class QuestionSet(models.Model):
    name = models.CharField(max_length=200, default='QuestionSet')
    times_taken = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/qset/%s" % self.name


class Interview(models.Model):
    candidate = models.ForeignKey(Candidate)
    date = models.DateField()
    position = models.ForeignKey(Position)
    question_set = models.ForeignKey(QuestionSet, null=True)
    status_choices = (
        ('AC', 'Active'),
        ('CN', 'Cancelled'),
        ('FN', 'Finished'),
                     )
    status = models.CharField( # This field can be shown in template as get_status_display
                        max_length=2,
                        choices=status_choices,
                        default='AC'
                             )

    # This is to mark if the candidate passed the test.
    result_choices = (
        ('P', 'Pass'),
        ('F', 'Fail'),
        ('TBD', 'Pending'),
                    )

    result = models.CharField( # This field can be shown in template as get_result_display
        max_length=3,
        choices=result_choices,
        default='TBD'
    )

    def __str__(self):  # __unicode__ on Python 2
        return "{0}_{1}_{2}".format(self.candidate, str(self.date), self.position)

    @classmethod
    def interviews_today(cls):
        return Interview.objects.filter(date=datetime.today())

    @classmethod
    def all_interviews(cls):
        return Interview.objects.all()

class Skill(models.Model):
    name = models.CharField('Name', max_length=20)
    position = models.ManyToManyField(Position)

    def __str__(self):  # __unicode__ on Python 2
        return self.name



class Question(models.Model):
    description = models.CharField('Description', max_length=300)
    difficulty_choice = (
        ('H', 'Hard'),
        ('M', 'Medium'),
        ('E', 'Easy'),
    )

    difficulty = models.CharField(
        max_length=3,
        choices=difficulty_choice,
        default='M'
                    )

    skill = models.ForeignKey(Skill, null=True)
    qset = models.ManyToManyField(QuestionSet)

    def __str__(self):  # __unicode__ on Python 2
        return "{0}".format(self.description)


class Answer(models.Model):
    """
    Answer's Model, which is used as the answer in Question Model
    """
    detail = models.CharField(max_length=128, verbose_name=u'Answer\'s text')
    question = models.ForeignKey(Question, null=True)
    correct = models.BooleanField('Correct', default=True)

    def __str__(self):
        return self.detail


