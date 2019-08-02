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
                else:
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
        student_form = CreateStudentForm(request.POST)
        if register_form.is_valid() and student_form.is_valid():

            user = register_form.save(commit = False)
            user.is_student = True
            user.save()
            student = student_form.save(commit = False)
            student.user = user
            student.save()
            
           
            
            if request.POST.get('save'):
                return redirect('teacher_home')
            elif request.POST.get('save_and_add_new'):
                return redirect('add_student')
    else:
       
        register_form = UserRegisterForm()
        student_form = CreateStudentForm()
        
    return render(request, 'add_student.html', {'register_form': register_form, 'student_form' : student_form})


def add_assignment(request):
    if request.method == 'POST':
        assignment_form = CreateAssignmentForm(request.POST)
        

        if assignment_form.is_valid():
            Assignment = assignment_form.save(commit=False)
            Assignment.save()
        return redirect('teacher_home')
    else:
        assignment_form = CreateAssignmentForm()
    return render(request, 'add_assignment.html', {
        'assignment_form': assignment_form})

def add_rubrik(request, pk):
    assignment =Assignment.objects.get(id = pk)

    if request.method == 'POST':
        form = CreateRubrikForm(request.POST)

        if form.is_valid():
            rubrik = form.save(commit=False)
            rubrik.assignment = assignment
            rubrik.save()
            return redirect('teacher_assignment_view', pk = pk)
    else:
        form = CreateRubrikForm()
    return render(request, 'add_rubrik.html', context = {
        'form': form,
        })

    


def teacher_home(request):
    students = Student.objects.all()
    assignments = Assignment.objects.all()
    header_row = ['Student']+[a.assignment_title for a in assignments]
    table_content = []
    

    for s in students:
        row_content = [s.user.username]
        for a in assignments:
            try:
                sub = Submission.objects.get(student__id = s.id, assignment_id = a.id)
                if sub.published_date <= a.submission_date:
                    cell_content = 'on time'
                else:
                    cell_content = 'late'
            except Submission.DoesNotExist:
                cell_content = ''

            row_content.append(cell_content)
        table_content.append(row_content)

        context = {'table_content': table_content,
                    'assignments': assignments,
                    'students' : students
                    }
    return render(request, 'teacher_home.html', context)


def teacher_assignment_view(request, pk):
    assignment = Assignment.objects.get(id = pk)
    try:
        peer_rubrik = Peer_review_rubrik.objects.filter(assignment = pk)
    except Peer_review_rubrik.DoesNotExist:
        peer_rubrik = None
    
    return render(request, 'teacher_assignment_view.html', context = {
        'assignment' : assignment,
        'peer_rubrik': peer_rubrik

    })
    

def teacher_patches(request):
    return render(request, 'teacher_patches.html')




def make_submission(request, pk):
    if request.method == 'POST':
        form = SubmissionForm(request.POST)

        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = Student.objects.get(user = request.user)
            submission.assignment = Assignment.objects.get(id = pk)
            submission.published_date = datetime.now()
            submission.save()
            return redirect('assignment_view', pk = pk)

        else:
            print(form.errors)
    else:
        form = SubmissionForm()

    return render(request, 'make_submission.html', context={'form': form})


def assignment_view(request, pk):
    assignment = Assignment.objects.get(pk = pk)
    
    try:
        submission = Submission.objects.get(student__user = request.user)
    except Submission.DoesNotExist:
        submission = None
    
    return render(request, 'assignment_view.html', context = { 
        'assignment': assignment, 
        'submission': submission })



def give_feedback(request, pk):
    user = Student.objects.get(user = request.user)
    own_group = user.group
    group_members = Student.objects.filter(group = own_group).exclude(user = request.user)
    
    assignment = Assignment.objects.get(id = pk)
    
    submissions = Submission.objects.filter( assignment__id = pk, student__in = group_members )

    return render(request, 'give_feedback.html', context = {
        'submissions' : submissions,
        'assignment' : assignment

        
    })

def group_submission(request, id, pk):
    assignment = Assignment.objects.get(pk = pk)
    submission = Submission.objects.get(id = id)
    author = Student.objects.get(user = request.user)
    

  
    
    peer_review = Peer_review_submission.objects.filter(author = author, submission = submission)
    peer_rubrik = Peer_review_rubrik.objects.filter(assignment = assignment).exclude(id__in= peer_review)
    #peer_rubrik = peer_rubrik.exclude(id__in = peer_review)
    

    
    

    form = PeerReviewForm()
    
    
    return render(request, 'group_submission.html', context = {
        'assignment' : assignment,
        'submission' : submission,
        'peer_rubrik' : peer_rubrik,
        'peer_review' : peer_review,
        'form' : form
         })


def submit_peer_review(request, id, pk, rubrik):
    submission = Submission.objects.get(id = id)
    author = Student.objects.get(user = request.user)
    peer_rubrik = Peer_review_rubrik.objects.get(id = rubrik)
    form = PeerReviewForm(request.POST)

    if form.is_valid():
            
        peer_review = form.save(commit=False)
        peer_review.submission = submission
        peer_review.author = author
        peer_review.date = datetime.now()
        peer_review.peer_review_rubrik = peer_rubrik
        peer_review.save()
    return redirect('group_submission', pk = pk, id = id)

def view_feedback(request, pk):
    return render(request, 'view_feedback.html')


def student_home(request):
    assignments = Assignment.objects.all()
    return render(request, 'student_home.html', context = {'assignments':assignments})
