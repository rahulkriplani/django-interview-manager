# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator
from datetime import datetime

class Position(models.Model):
    name = models.CharField(max_length=50)
    id_code = models.CharField(max_length=10)

    def __str__(self):  # __unicode__ on Python 2
        return self.name

class Candidate(models.Model):
    name = models.CharField(max_length=40)
    contact_primary = RegexValidator(regex='^\d{10}$')
    contact_secondary = RegexValidator(regex='^\d{10}$')
    experience = models.PositiveIntegerField()
    position_applied = models.ForeignKey(Position)

    def __str__(self):  # __unicode__ on Python 2
        return self.name

class Interview(models.Model):
    candidate = models.ForeignKey(Candidate)
    date = models.DateField()
    position = models.ForeignKey(Position)

    def __str__(self):  # __unicode__ on Python 2
        return "{0}_{1}_{2}".format(self.candidate, str(self.date), self.position)

    def interviews_today(self):
        return Interview.objects.filter(date=datetime.today())

    def all_interviews(self):
        return Interview.objects.all()

