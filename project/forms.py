from django import forms
from project.models import User
from project.models import Submission, User, Patch  # , Peer_rubrik
from tinymce.widgets import TinyMCE
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class SubmissionForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )

    class Meta:
        model = Submission
        fields = ['content']


class UserRegisterForm(UserCreationForm):
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)
        #def __init__(self, *args, **kwargs):
         #   super(myUserCreationForm, self).__init__(*args, **kwargs)

           # self.fields['username'].widget.attrs['class'] = 'form-control'
           # self.fields['password1'].widget.attrs['class'] = 'form-control'
           # self.fields['password2'].widget.attrs['class'] = 'form-control'


class UserEditForm(UserChangeForm):
    email = forms.CharField(max_length = 100)
    class Meta(UserChangeForm):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)




   
class CreatePatchForm(forms.ModelForm):
    class Meta:
        model = Patch
        fields = ('name', 'start_date',  'submission_date', 'peer_review_date')


class CreateAssessmentForm(forms.ModelForm):
    class Meta:
        model = Patch
        fields = ('assignment_title', 'assignment_description')

# class CreateRubrikForm(forms.ModelForm):
#     class Meta:
#         model = Peer_rubrik
#         fields = ('peer_rubrik_text',)


# class CreatePatchesForm(forms.ModelForm):
#     class Meta:
#         model = Patch
#         fields = ['']
