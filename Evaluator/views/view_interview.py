from modules import *

#***********************************************************************
#-------------------------------- INTERVIEW ---------------------------
#***********************************************************************

@user_passes_test(lambda u: u.is_staff)
@login_required
def all_interviews(request):
    interviews = Interview.objects.get_queryset().order_by('id')
    interview_filter = InterviewFilter(request.GET, queryset=interviews)

    page = request.GET.get('page', 1)
    paginator = Paginator(interview_filter.qs, 10)
    try:
        page_interviews = paginator.page(page)
    except PageNotAnInteger:
        page_interviews = paginator.page(1)
    except EmptyPage:
        page_interviews = paginator.page(paginator.num_pages)

    return render(request, 'all_interviews.html', {'filter': interview_filter, 'interviews': page_interviews})


@user_passes_test(lambda u: u.is_staff)
@login_required
def add_interview(request):
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

    return render(request, 'details_interview.html', args)



@user_passes_test(lambda u: u.is_staff)
@login_required
def edit_interview(request, interview_pk):
    interview = Interview.objects.get(pk=interview_pk)
    form = forms.AddInterview(instance=interview)
    round_forms = forms.RoundInLineFormSet(
            queryset=form.instance.round_set.all()
            )
    if request.method == 'POST':
        form = forms.AddInterview(request.POST, instance=interview)
        round_forms = forms.RoundInLineFormSet(
                request.POST,
                queryset=form.instance.round_set.all()
                )
        if form.is_valid() and round_forms.is_valid():
            form.save()
            rnds = round_forms.save(commit=False)
            for rnd in rnds:
                rnd.interview = interview
                rnd.save()
            return HttpResponseRedirect(interview.get_absolute_url())
    return render(request, 'add_interview.html',
            {
                'form':form,
                'formset':round_forms
            })

