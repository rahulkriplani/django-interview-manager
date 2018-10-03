from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from . import models

class AddRatingForRound(forms.ModelForm):

    def __init__(self, round_list, *args, **kwargs):
        super(AddRatingForRound, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.ChoiceField(choices=tuple([(name, name) for name in round_list]))

    #round_name = forms.CharField(label='Round Name', max_length=100)
    class Meta:
        model = models.RatingSheet
        fields = ('name', )


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2' )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False) # Don't save it yet
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=False) # Don't save it yet
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class AnswerForm(forms.ModelForm):
    class Meta:
        models = models.Answer
        fields = ['detail', 'correct']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ['description', 'difficulty', 'skill', 'qset']

AnswerFormSet = forms.modelformset_factory(
        models.Answer,
        form=AnswerForm,
        extra=2
                                            )

AnswerInLineFormSet = forms.inlineformset_factory(
        models.Question,
        models.Answer,
        extra=2,
        fields=('detail', 'correct'),
        formset=AnswerFormSet,
        min_num=1,
        )

class AddCandidateForm(forms.ModelForm):
    class Meta:
        model = models.Candidate
        fields = ['name', 'experience', 'position_applied', 'contact_primary', 'vendor']

class QuestionSetForm(forms.ModelForm):
    name = forms.CharField(max_length=200)
    class Meta:
        model = models.QuestionSet
        fields = ['name',]

class AddInterview(forms.ModelForm):
    class Meta:
        model = models.Interview
        fields = ['candidate', 'date', 'position', 'question_set']

class RoundForm(forms.ModelForm):
    class Meta:
        models = models.Round
        fields = ['name', 'date', 'contact_time', 'assignee', 'round_type', 'result']

RoundFormSet = forms.modelformset_factory(
        models.Round,
        form=RoundForm,
        extra=0
        )

RoundInLineFormSet = forms.inlineformset_factory(
        models.Interview,
        models.Round,
        extra=1,
        fields=('name', 'date', 'contact_time', 'assignee', 'round_type', 'result'),
        formset=RoundFormSet,
        min_num=0,
        )
