from modules import *


#***********************************************************************
#-------------------------------- CANDIDATE ---------------------------
#***********************************************************************

@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/login")
def add_candidate(request):
    if request.method == 'POST':
        form = forms.AddCandidateForm(request.POST)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.name = form.cleaned_data['name']
            candidate.contact_primary = form.cleaned_data['contact_primary']
            candidate.experience = form.cleaned_data['experience']
            candidate.position_applied = form.cleaned_data['position_applied']
            candidate.save()
            for sk in form.cleaned_data['skill']:
                skill = Skill.objects.get(name=sk)
                candidate.skill.add(skill)

            return HttpResponseRedirect(candidate.get_absolute_url())
    else:
        form = forms.AddCandidateForm()
        args = {'form': form}
        return render(request, 'add_candidate.html', args)


@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/login")
def all_candidates(request):
    candidates = Candidate.objects.get_queryset().order_by('id')
    candidate_filter = CandidateFilter(request.GET, queryset=candidates)
    page = request.GET.get('page', 1)
    paginator = Paginator(candidate_filter.qs, 10)
    try:
        page_candidates = paginator.page(page)
    except PageNotAnInteger:
        page_candidates = paginator.page(1)
    except EmptyPage:
        page_candidates = paginator.page(paginator.num_pages)

    return render(request, 'all_candidates.html', {'candidates': page_candidates, 'filter': candidate_filter})


@login_required(login_url="/login")
@user_passes_test(lambda u: u.is_staff)
def edit_candidate(request, candidate_pk):
    candidate = Candidate.objects.get(pk=candidate_pk)
    if request.method == 'POST':
        form = forms.AddCandidateForm(request.POST, instance=candidate)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(candidate.get_absolute_url())
    else:
        form = forms.AddCandidateForm(instance=candidate)
        args = {'form':form}
        return render(request, 'add_candidate.html', args)


@login_required(login_url="/login")
@user_passes_test(lambda u: u.is_staff)
def candi_details(request, candidate_pk):
    candidate = Candidate.objects.get(pk=candidate_pk)
    interviews = Interview.objects.filter(candidate=candidate)
    args = {'candidate': candidate, 'interviews': interviews}
    return render(request, 'details_candidate.html', args)
