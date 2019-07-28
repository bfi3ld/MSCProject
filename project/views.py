from django.shortcuts import render, redirect
from django.http import HttpResponse
from project.forms import *
from django.utils.timezone import datetime
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView
from project.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request, 'index.html')


def teacher_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():

            user = form.save(commit=False)
            #user.refresh_from_db()
            user.is_teacher = True
            user.save()
            
            return redirect('index')
    else:
       
        form = UserRegisterForm()
    return render(request, 'teacher_register.html', {'form': form})

def log_in(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_student:
                    return redirect('student_home')
                elif user.is_teacher:
                    return redirect('teacher_home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    return render(request = request,
                    template_name = "login.html",
                    context={"form":form})


    
    
def add_student(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
       
        if form.is_valid():

            user = form.save()
            user.is_student = True
            user.save()
            return redirect('teacher_home')
    else:
       
        form = UserRegisterForm()
    return render(request, 'add_student.html', {'form': form})


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
    all_students = User.objects.filter(is_student = True)
    all_patches = Patch.objects.all()
    header_row = ['Student']+[p.name for p in all_patches]
    table_content = []

    for s in all_students:
        row_content = [s.username]
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
            submission.student = request.user
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


def student_home(request):
    return render(request, 'student_home.html')
