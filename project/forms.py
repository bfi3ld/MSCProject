from django import forms
from project.models import User
from project.models import Submission, User, Patch, Student, Peer_review_rubrik, Feedback, Submission_edits

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm
from django_summernote.widgets import SummernoteWidget




class SubmissionForm(forms.ModelForm):
    content = forms.CharField(widget=SummernoteWidget())

    class Meta:
        model = Submission
        fields = ['content',]

class EditSubmissionForm(forms.Form):
    content = forms.CharField(widget=SummernoteWidget())
    


class UserRegisterForm(UserCreationForm):
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-style'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-style'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-style'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-style'}))
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)
  

class CreateStudentForm(forms.ModelForm):
    group = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-style'}))

    class Meta():
        model = Student
        fields = {'group',}
        

class UserEditForm(UserChangeForm):
    email = forms.CharField(max_length = 100)
    class Meta(UserChangeForm):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget = forms.TextInput(attrs = {'class' : 'login_fields', 'placeholder' : 'Username',}))
    password = forms.CharField(widget = forms.PasswordInput(attrs = {'class' : 'login_fields', 'placeholder' : 'Password'}))



class CreatePatchForm(forms.ModelForm):
    patch_title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-style'}))
    patch_description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-text-style'}))
    submission_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-style'}))
    peer_review_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-style'}))


    class Meta:
        model = Patch
        fields = ('patch_title', 'patch_description', 'submission_date', 'peer_review_date')

class CreateRubrikForm(forms.ModelForm):
    instruction = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-text-style'}))
    class Meta:
        model = Peer_review_rubrik
        fields = ('instruction',)


class PeerReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-style'}))
    
    class Meta:
        model = Feedback
        fields = ('review',)


