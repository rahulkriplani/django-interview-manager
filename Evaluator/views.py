# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Interview

# Create your views here.
def index(request):
    return render(request, 'home.html')

def profile(request):
    i = Interview()
    print i.interviews_today()
    args = {'user':request.user, 'interview_today': i.interviews_today()}
    return render(request, 'profile.html')