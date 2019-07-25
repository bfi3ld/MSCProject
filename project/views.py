from django.shortcuts import render, redirect
from django.http import HttpResponse
from project.forms import *
from django.utils.timezone import datetime
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView
from project.models import User
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def index(request):
    return render(request, 'index.html')


def teacher_register(request):
    if request.method == 'POST':
        form = TeacherRegisterForm(request.POST)
        user_form = UserCreationForm(request.POST)
        if form.is_valid() and user_form.is_valid():

            teacher = form.save(commit=False)
            user = user_form.save()
            teacher.user = user
            teacher.save()
            return redirect('index.html')
    else:
        user_form = UserCreationForm()
        form = TeacherRegisterForm()
    return render(request, 'teacher_register.html', {'form': form, 'user_form': user_form})


def add_patch(request):
    if request.method == 'POST':
        patch_form = CreatePatchForm(request.POST)
        assessment_form = CreateAssessmentForm(request.POST)

        if patch_form.is_valid() and assessment_form.is_valid():
            Patch = patch_form.save(commit=False)
            Assessment = assessment_form.save()
            Patch.assessment = assessment
            Patch.save()
        return redirect()
    else:
        patch_form = CreatePatchForm()
        assessment_form = CreateAssessmentForm()
    return render(request, 'teacher_home.html', {'p_form': patch_form, 'a_form': assessment_form})


def teacher_home(request):
    all_students = Student.objects.all()
    all_patches = Patch.objects.all()
    header_row = ['Student']+[p.name for p in all_patches]
    table_content = []

    for s in all_students:
        row_content = [s.name]
        for p in all_patches:
            try:
                sub = Submission.objects.get(student__id=s.id, patch__name=p.name)
                if sub.published_date <= p.submission_date:
                    cell_content = 'on time'
                else:
                    cell_content = 'late'
            except Submission.DoesNotExist:
                cell_content = ''

            row_content.append(cell_content)
        table_content.append(row_content)

    context = {'header_row': header_row, 'table_content': table_content}
    return render(request, 'teacher_home.html', context)


def teacher_patches(request):
    return render(request, 'teacher_patches.html')


def make_submission(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST)

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
