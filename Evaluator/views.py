# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.utils import timezone

from . import forms
from .models import Interview, Question, Candidate, Answer, QuestionSet, Round, Vendor
from .filters import InterviewFilter, CandidateFilter


def add_ratings(request):
    if request.method == 'POST':
        form = forms.AddRatingForRound(request.POST)
        if form.is_valid():
            print 'Form is good'
            return redirect('/profile')
    else:
        form = forms.AddRatingForRound()
    return render(request, 'add_rating.html', {'form': form })


def index(request):
    return render(request, 'Evaluator/home.html')


def customForm(request, interview_pk):
    if request.method == 'GET':
        try:
            interview = Interview.objects.get(pk=interview_pk)
        except Interview.DoesNotExist:
            raise Http404("Interview does not exists!")

        count_rounds = range(Round.objects.filter(interview__pk=interview_pk).count())
        return render(request, 'CustomForm.html', {'r_count': count_rounds})

def customFormProcess(request):
    #interview = Interview.objects.get(pk=interview_pk)

    print request.POST


#***********************************************************************
#-------------------------------- USER ---------------------------
#***********************************************************************

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
        # Redirecting to the required login according to user status.
            if user.is_superuser or user.is_staff:
                login(request, user)
                return redirect('/profile')  # or your url name
            else:
                login(request, user)
                return render(request, 'exam_launch.html')
        else:
            return render(request, 'login_form.html', {'error': 'Incorrect password'})
    else:
        return render(request, 'login_form.html')

@user_passes_test(lambda u: u.is_staff)
@login_required
def profile(request):
    today_date = timezone.now().date()
    user_rounds = Round.objects.filter(assignee=request.user, date__gte=today_date, interview__status='AC')
    args = {'user': request.user, 'my_rounds': user_rounds}
    return render(request, 'profile.html', args)

def register(request):
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = forms.RegistrationForm()
        args = {'form': form}
        return render(request, 'register.html', args)

@user_passes_test(lambda u: u.is_staff)
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = forms.EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/profile')
    else:
        form = forms.EditProfileForm(instance=request.user)
        args = {'form' : form}
        return render(request, 'edit_profile.html', args)

def change_password(request):
    if request.method == 'POST':
        form = forms.PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/profile')
        else:
            return redirect('/profile/password')
    else:
        form = forms.PasswordChangeForm(user=request.user)
        args = {'form':form}
        return render(request, 'password_change.html', args)

#***********************************************************************
#-------------------------------- INTERVIEW ---------------------------
#***********************************************************************

@user_passes_test(lambda u: u.is_staff)
@login_required
def all_interviews(request):
    interviews = Interview.all_interviews()
    interview_filter = InterviewFilter(request.GET, queryset=interviews)
    return render(request, 'all_interviews.html', {'interviews': interviews, 'filter': interview_filter})


@user_passes_test(lambda u: u.is_staff)
@login_required
def add_interview(request):
    """
    if request.method == 'POST':
        form = forms.AddInterview(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('/profile')
    else:
        form = forms.AddInterview()
        args = {'form': form}
        return render(request, 'add_interview.html', args)
    """

    round_forms = forms.RoundInLineFormSet(
            queryset=Round.objects.none()
            )
    form = forms.AddInterview()
    if request.method == 'POST':
        form = forms.AddInterview(request.POST)
        round_forms = forms.RoundInLineFormSet(
                request.POST,
                queryset=Round.objects.none()
                )
        if form.is_valid() and round_forms.is_valid():
            interview = form.save()
            rounds = round_forms.save(commit=False)
            for a_round in rounds:
                a_round.interview = interview
                a_round.save()
            return HttpResponseRedirect(interview.get_absolute_url())
    return render(request, 'add_interview.html',
            {
                'form':form,
                'formset':round_forms
            })


@user_passes_test(lambda u: u.is_staff)
@login_required
def interviews_details(request, interview_pk):
    try:
        interview = Interview.objects.get(pk=interview_pk)
    except Interview.DoesNotExist:
        raise Http404("Interview does not exists!")

    all_rounds = interview.round_set.order_by('created_at')
    args = {'interview': interview, 'rounds': all_rounds}

    return render(request, 'interview_details.html', args)



@login_required
def question_detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exists!")
    args = {'question': question}
    return render(request, 'question_details.html', args)

#***********************************************************************
#-------------------------------- CANDIDATE ---------------------------
#***********************************************************************


@user_passes_test(lambda u: u.is_staff)
@login_required
def add_candidate(request):
    if request.method == 'POST':
        form = forms.AddCandidateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.name = form.cleaned_data['name']
            post.contact_primary = form.cleaned_data['contact_primary']
            post.experience = form.cleaned_data['experience']
            post.position_applied = form.cleaned_data['position_applied']
            post.save()
            return redirect('/profile')
    else:
        form = forms.AddCandidateForm()
        args = {'form': form}
        return render(request, 'add_candidate.html', args)

@user_passes_test(lambda u: u.is_staff)
@login_required
def search_candidate(request):
    if request.method == 'GET':
        if 'keyword' in request.GET.keys():
            keyword = request.GET['keyword']
            candis = Candidate.objects.filter(name__icontains=keyword)
            if candis:
                return render(request, 'search_candidate.html', {'candi_list': candis})
            else:
                return render(request, 'search_candidate.html', {'error_message': 'No candidates matching'})
        else:
            return render(request, 'search_candidate.html')

@user_passes_test(lambda u: u.is_staff)
@login_required
def all_candidates(request):
    candidates = Candidate.objects.all()
    candidate_filter = CandidateFilter(request.GET, queryset=candidates)
    return render(request, 'all_candidates.html', {'candidates': candidates, 'filter': candidate_filter})

@login_required
def edit_candidate(request, candidate_pk):
    candidate = Candidate.objects.get(pk=candidate_pk)
    if request.method == 'POST':
        form = forms.AddCandidateForm(request.POST, instance=candidate)
        if form.is_valid():
            form.save()
            return redirect('/profile')  # This has to go to candidate details page
    else:
        form = forms.AddCandidateForm(instance=candidate)
        args = {'form':form}
        return render(request, 'edit_profile.html', args)

def candi_details(request, candidate_pk):
    candidate = Candidate.objects.get(pk=candidate_pk)
    interviews = Interview.objects.filter(candidate=candidate)
    args = {'candidate': candidate, 'interviews': interviews}
    return render(request, 'candi_details.html', args)

#***********************************************************************
#-------------------------------- QUESTION ---------------------------
#***********************************************************************


@user_passes_test(lambda u: u.is_staff)
@login_required
def search_question(request):
    if request.method == 'GET':
        if 'keyword' in request.GET.keys():
            keyword = request.GET['keyword']
            questions = Question.objects.filter(description__icontains=keyword)
            if questions:
                return render(request, 'search_candidate.html', {'question_list': questions})
            else:
                return render(request, 'search_candidate.html', {'error_message': 'No candidates matching'})
        else:
            return render(request, 'search_candidate.html')



@method_decorator(login_required, name='dispatch')
class QuestionList(ListView):
    model = Question

@user_passes_test(lambda u: u.is_staff)
@login_required
def create_question(request):
    answer_forms = forms.AnswerInLineFormSet(
            queryset=Answer.objects.none()
            )
    form = forms.QuestionForm()
    if request.method == 'POST':
        form = forms.QuestionForm(request.POST)
        answer_forms = forms.AnswerInLineFormSet(
                request.POST,
                queryset=Answer.objects.none()
                )
        if form.is_valid() and answer_forms.is_valid():
            question = form.save()
            answers = answer_forms.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()
            #return HttpResponseRedirect(reverse('Evaluator:profile'))
            return HttpResponseRedirect(question.get_absolute_url())
    return render(request, 'create_question.html',
            {
                'form':form,
                'formset':answer_forms
            })

@user_passes_test(lambda u: u.is_staff)
@login_required
def edit_question(request, que_pk):
    question = Question.objects.get(pk=que_pk)
    form = forms.QuestionForm(instance=question)
    answer_forms = forms.AnswerInLineFormSet(
            queryset=form.instance.answer_set.all()
            )
    if request.method == 'POST':
        form = forms.QuestionForm(request.POST, instance=question)
        answer_forms = forms.AnswerInLineFormSet(
                request.POST,
                queryset=form.instance.answer_set.all()
                )
        if form.is_valid() and answer_forms.is_valid():
            form.save()
            answers = answer_forms.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()
            return HttpResponseRedirect(question.get_absolute_url())
    return render(request, 'create_question.html',
            {
                'form':form,
                'formset':answer_forms
            })

#***********************************************************************
#-------------------------------- QUESTION SET -------------------------
#***********************************************************************


@user_passes_test(lambda u: u.is_staff)
@login_required
def create_question_set(request):
    question_set_form = forms.QuestionSetForm()
    if request.method == 'POST':
        question_set_form = forms.QuestionSetForm(request.POST)
        if question_set_form.is_valid():
            question_set = question_set_form.save()
            return HttpResponseRedirect(question_set.get_absolute_url())
    return render(request, 'create_exam.html',
            {
                'form':question_set_form
            })

def question_set_details(request, qset_pk):
    question_set = QuestionSet.objects.get(pk=qset_pk)
    questions = Question.objects.filter(qset=question_set)
    return render(request, 'qset_details.html', {'question_set': question_set, 'questions':questions})

@login_required
def get_question_sets(request):
    question_sets = QuestionSet.objects.all()
    return render(request, 'all_qsets.html',{'question_sets':question_sets})

@login_required
def question_sets(request):
    question_sets = QuestionSet.objects.all()
    return render(request, 'all_qsets.html',{'question_sets':question_sets})

#***********************************************************************
#-------------------------------- EXAM ---------------------------
#***********************************************************************

@user_passes_test(lambda u: u.is_staff)
@login_required
def exams(request):
    Exams = Exam.objects.all()
    return render(request, 'exams.html',{'exams':Exams})

@login_required
def exam_launch_page(request):
    return render(request, 'exams_launch.html')


#***********************************************************************
# -------------------------------- Vendor ---------------------------
#***********************************************************************

@user_passes_test(lambda u: u.is_staff)
@login_required
def allVendors(request):
    return render(request, 'all_vendors.html', {'vendors': Vendors.objects.all()})

@user_passes_test(lambda u: u.is_staff)
@login_required
def vendor_details(request, vendor_pk):
    vendor = Vendor.objects.get(pk=vendor_pk)
    return render(request, 'vendors_details.html', {'vendor': vendor})


