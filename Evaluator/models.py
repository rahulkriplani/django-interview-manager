# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator

class Position(models.Model):
    name = models.CharField(max_length=50)
    id_code = models.CharField(max_length=10)

class Interview(models.Model):
    candidate = models.OneToOneField(User)
    date = models.DateField()
    position = models.OneToOneField(Position)

class Candidate(models.Model):
    name = models.CharField(max_length=40)
    contact_primary = RegexValidator(regex='^\d{10}$')
    contact_secondary = RegexValidator(regex='^\d{10}$')
    experience = models.IntegerField()
    position_applied = models.OneToOneField(Position)