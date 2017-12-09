# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Interview
from .forms import RegistrationForm

# Create your views here.
def index(request):
    return render(request, 'home.html')

def profile(request):
    i = Interview()
    print i.interviews_today()

    args = {'user':request.user, 'interview_today': i.interviews_today()}
    return render(request, 'profile.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = RegistrationForm()
        args = {'form': form}
        return render(request, 'register.html', args)

