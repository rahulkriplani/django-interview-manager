# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator
from django.shortcuts import redirect
from django.utils import timezone
from simple_history.models import HistoricalRecords
from django.core.urlresolvers import reverse

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

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_validator = RegexValidator(regex='\d+')
    phone_number = models.CharField(max_length=20, validators=[contact_validator], null=True)
    address = models.TextField()
    type_choices = (
        ('O', 'Online'),
        ('R', 'Reference'),
        ('RS', 'Recruitment Service'),
        ('OT', 'Other'),
        ('N', 'None')
                     )
    v_type = models.CharField( # This field can be shown in template as get_status_display
                        max_length=2,
                        choices=type_choices,
                        default='N'
                             )

    def __str__(self):  # __unicode__ on Python 2
        return self.name

    def get_absolute_url(self):
        return reverse('vendor_details', args=[str(self.id)])


class Candidate(models.Model):
    name = models.CharField(max_length=40)
    contact_validator = RegexValidator(regex='\d+')
    contact_primary = models.CharField(max_length=20, validators=[contact_validator], null=True)
    experience = models.PositiveIntegerField()
    position_applied = models.ForeignKey(Position)
    vendor = models.ForeignKey(Vendor, null=True)


    def __str__(self):  # __unicode__ on Python 2
        return self.name

    def get_absolute_url(self):
        return reverse('candi_details', args=[str(self.id)])



class QuestionSet(models.Model):
    name = models.CharField(max_length=200, default='QuestionSet')
    times_taken = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Evaluator:question_set_details', args=[str(self.id)])


class Interview(models.Model):
    candidate = models.ForeignKey(Candidate)
    date = models.DateField()
    position = models.ForeignKey(Position)
    question_set = models.ForeignKey(QuestionSet, null=True, blank=True)
    history = HistoricalRecords()
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
        ('S', 'Selected'),
        ('R', 'Rejected'),
        ('J', 'Joined'),
        ('DNJ', 'Did Not Join'),
        ('TBD', 'Pending'),
                    )

    result = models.CharField( # This field can be shown in template as get_result_display
        max_length=3,
        choices=result_choices,
        default='TBD'
    )

    def __str__(self):  # __unicode__ on Python 2
        return "{0}_{1}_{2}".format(self.candidate, str(self.date), self.position)

    def get_absolute_url(self):
        return reverse('Evaluator:interview_details', args=[str(self.id)])

    @classmethod
    def interviews_today(cls):
        return Interview.objects.filter(date=datetime.today())

    @classmethod
    def all_interviews(cls):
        return Interview.objects.all()



class Round(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    contact_time = models.TimeField(default=timezone.now)
    assignee = models.ForeignKey(User)
    interview = models.ForeignKey(Interview)
    created_at = models.DateTimeField(default=datetime.now, editable=False)
    modified_on = models.DateTimeField(default=datetime.now, editable=False)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.modified_on = timezone.now()
        return super(Round, self).save(*args, **kwargs)

    type_choices = (
        ('U', 'Undecided'),
        ('F2F', 'Face to Face'),
        ('SKYPE', 'Skype Call'),
        ('TP', 'Telephonic'),
        ('VC', 'Client Video Call'),
        ('FD', 'Final Discussion'),
        ('HR', 'HR Discussion'),
        ('Other', 'Other Types'),
                    )

    round_type = models.CharField( # This field can be shown in template as get_status_display
                        max_length=10,
                        choices=type_choices,
                        default='U'
                             )

    result_choice = (
        ('ADV', 'Advanced'),
        ('RJ', 'Rejected'),
        ('CN', 'Cancelled'),
        ('DNA', 'Did Not Appear'),
        ('DNO', 'Did Not Accept Offer'),
        ('RS', 'Rescheduled'),
        ('W', 'Waiting'),
        ('S', 'Selected'),
        ('OH', 'On Hold'),
                    )

    result = models.CharField( # This field can be shown in template as get_status_display
                        max_length=5,
                        choices=result_choice,
                        default='W'
                             )

    def __str__(self):  # __unicode__ on Python 2
        return "{0}_{1}".format(self.name, str(self.date), self.round_type)


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

    def get_absolute_url(self):
        return reverse('Evaluator:question_detail', args=[str(self.id)])


class Answer(models.Model):
    """
    Answer's Model, which is used as the answer in Question Model
    """
    detail = models.CharField(max_length=128, verbose_name=u'Answer\'s text')
    question = models.ForeignKey(Question, null=True)
    correct = models.BooleanField('Correct', default=True)

    def __str__(self):
        return self.detail


