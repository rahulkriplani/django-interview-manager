from modules import *

#***********************************************************************
#-------------------------------- USER ---------------------------
#***********************************************************************


def user_login(request):
    if request.user.is_authenticated():
        return redirect('/profile')

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

@user_passes_test(lambda u: u.is_staff)
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/profile')
        else:
            return redirect('/profile/password')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form':form}
        return render(request, 'password_change.html', args)

@user_passes_test(lambda u: u.is_staff)
@login_required
def get_details_user(request, user_pk):
    user = User.objects.get(pk=user_pk)
    if user:
        rounds = user.round_set.all()
        return render(request, 'details_user.html', {'rounds': rounds, 'user': user})
    else:
        raise Http404("User does not exists!")
