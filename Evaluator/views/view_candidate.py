from modules import *



#***********************************************************************
#-------------------------------- CANDIDATE ---------------------------
#***********************************************************************

def create_candis_interviews(fileobj):

    for row in fileobj:
        candi =  [row.strip() for row in row.split(',')]
        # Create a candidate
        print candi
        position = Position.objects.get(id_code=candi[1].strip())
        vendor = Vendor.objects.get(name=candi[4])
        candidate = Candidate.objects.create(name=candi[0], position_applied=position, experience=candi[2], contact_primary=candi[3], vendor=vendor)

@user_passes_test(lambda u: u.is_staff)
@login_required(login_url="/login")
def bulk_upload_candis(request):
    # Note: Each line in csv file should be of format:
    # Oneil, SDE04, 8, 1122334455, Company Online
    # Name, Position, Exp, Contact, Vendor Name
    if request.method == 'POST':
        form = forms.BulkCreateCandidateForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file'].file

            create_candis_interviews(file)

            return render(request, 'success_bulk_upload.html')
        else:
            print 'Invalid form'
            return
    else:
        form = forms.BulkCreateCandidateForm()
        args = {'form': form}
        return render(request, 'bulk_upload_candis.html', args)

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
