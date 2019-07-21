from django import forms
from project.models import Submission
from tinymce import TinyMCE


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
        