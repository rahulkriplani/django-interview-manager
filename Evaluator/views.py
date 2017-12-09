# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from .models import Interview
from .forms import RegistrationForm, EditProfileForm
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.
def index(request):
    return render(request, 'home.html')

def profile(request):
    i = Interview()
    print i.interviews_today()

    args = {'user':request.user, 'interview_today': i.all_interviews()}
    return render(request, 'profile.html', args)

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

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/profile')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form':form}
        return render(request, 'edit_profile.html', args)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('/profile')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form':form}
        return render(request, 'password_change.html', args)

