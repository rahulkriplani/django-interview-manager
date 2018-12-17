from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse, render_to_response
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import TruncMonth
from django.db.models import Sum, Count

from Evaluator import forms
from Evaluator.models import Interview, Question, Candidate, Answer, QuestionSet, Round, Vendor
from Evaluator.models import RatingAspect, InterviewRatingSheet
from Evaluator.filters import InterviewFilter, CandidateFilter


from Evaluator.search import global_search
from Evaluator.mycalendar import InterviewCalendar

import json
import logging
import datetime

logger = logging.getLogger('mylogs')
