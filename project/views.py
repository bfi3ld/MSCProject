from django.shortcuts import render
from django.http import HttpResponse
from project.forms import SubmissionForm
from django.utils.timezone import datetime

# Create your views here.

def index(request):
    return render(request, 'index.html')


def make_submission(request):
    form = SubmissionForm(request.POST)
    

    if request.method == 'POST':
        

        if form.is_valid():
            submission = form.save(commit=False)
            #submission.student = request.user
            submission.published_date = datetime.now()
            submission.save()

             
        else:
            print(form.errors)
    else:
        form = SubmissionForm()
   

    return render(request, 'make_submission.html', context={'form': form})



def patch(request):
    return render(request, 'patch.html')

def assessment(request):
    return render(request, 'assessment.html')

def give_feedback(request):
    return render(request, 'give_feedback.html')

def view_feedback(request):
    return render(request, 'view_feedback.html') 