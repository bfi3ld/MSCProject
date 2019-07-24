from django import forms
from django.contrib.auth.models import User
from project.models import Submission, Student, Teacher, Patch, Assessment, Peer_rubrik
from tinymce.widgets import TinyMCE

from django.db import transaction

class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False

class SubmissionForm(forms.ModelForm):
    content= forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )


    class Meta:
        model = Submission
        fields =['content']
        

class TeacherRegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = Teacher
        fields = ('first_name', 'last_name', 'email',)


class CreatePatchForm(forms.ModelForm):
    class Meta:
        model = Patch
        fields = ('name', 'start_date', 'end_date', 'submission_date', 'peer_review_date')


class CreateAssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ('title', 'assessment')

class CreateRubrikForm(forms.ModelForm):
    class Meta:
        model = Peer_rubrik
        fields = ('peer_rubrik_text',)


# class CreatePatchesForm(forms.ModelForm):
#     class Meta:
#         model = Patch
#         fields = ['']
    
    


