from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from Evaluator import forms
from Evaluator.models import Interview, Question, Candidate, Answer, QuestionSet, Round, Vendor
from Evaluator.models import RatingAspect, InterviewRatingSheet
from Evaluator.filters import InterviewFilter, CandidateFilter

from Evaluator.search import global_search

import json
import logging

logger = logging.getLogger('mylogs')
