# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render(request, 'home.html')

def profile(request):
    args = {'user':request.user}
    return render(request, 'profile.html')