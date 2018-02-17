from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Question, Answer, Candidate

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

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['description', 'difficulty', 'skill']

#    def __init__(self, *args, **kwargs):
#        user = kwargs.pop('user', '')
#        super(QuestionForm, self).__init__(*args, **kwargs)
#        #self.fields['answer'] = forms.ModelChoiceField(queryset=Answer.objects.all())
#        self.fields['answer'] = forms.CharField(max_length=300)
#        self.fields['correct'] = forms.BooleanField()

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['detail', 'correct']

AnswerFormSet = forms.inlineformset_factory(Question, Answer,
                                            form=AnswerForm, extra=1)

class AddCandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['name', 'experience', 'position_applied', 'contact_primary']


class SearchCandidate(forms.Form):
    pass

