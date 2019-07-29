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
        register_form = UserRegisterForm(request.POST)
        
       
        if register_form.is_valid():

            user = register_form.save(commit = False)
            user.is_student = True
            user.save()
            if request.POST.get('save'):
                return redirect('teacher_home')
            elif request.POST.get('save_and_add_new'):
                return redirect('add_student')
    else:
       
        register_form = UserRegisterForm()
        
    return render(request, 'add_student.html', {'register_form': register_form})


def add_assignment(request):
    if request.method == 'POST':
        assignment_form = CreateAssignmentForm(request.POST)
        

        if assignment_form.is_valid():
            Assignment = assignment_form.save(commit=False)
            Assignment.save()
        return redirect('teacher_home')
    else:
        assignment_form = CreateAssignmentForm()
    return render(request, 'add_assignment.html', {'assignment_form': assignment_form})


def teacher_home(request):
    students = User.objects.filter(is_student = True)
    assignments = Assignment.objects.all()
    header_row = ['Student']+[a.assignment_title for a in assignments]
    table_content = []
    

    for s in students:
        row_content = [s.username]
        for a in assignments:
            try:
                sub = Submission.objects.get(student__id = s.id, assignment = a.assignment_title)
                if sub.published_date <= a.submission_date:
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
