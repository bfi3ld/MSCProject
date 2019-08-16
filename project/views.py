from django.shortcuts import render, redirect
from django.http import HttpResponse
from project.forms import *
from project.acj import update_values,calc_probability
from django.utils.timezone import datetime
from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView
from project.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib import messages
from diff_match_patch import diff_match_patch


# Create your views here.
def index(request):
    return render(request, 'index.html')


def teacher_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            # user.refresh_from_db()
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
    return render(request=request,
                  template_name="login.html",
                  context={"form": form})


def add_student(request):
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)
        student_form = CreateStudentForm(request.POST)
        if register_form.is_valid() and student_form.is_valid():

            user = register_form.save(commit=False)
            user.is_student = True
            user.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()

            if request.POST.get('save'):
                return redirect('teacher_home')
            elif request.POST.get('save_and_add_new'):
                return redirect('add_student')
    else:

        register_form = UserRegisterForm()
        student_form = CreateStudentForm()

    return render(request, 'add_student.html', {'register_form': register_form, 'student_form': student_form})


def add_assignment(request):
    if request.method == 'POST':
        assignment_form = CreateAssignmentForm(request.POST)

        final_assignment, created = Assignment.objects.get_or_create(
            is_final=True)
        if created:
            final_assignment.assignment_title = "Final Assignment"
            final_assignment.assignment_description = "final assignment"
            final_assignment.save()

        if assignment_form.is_valid():
            assignment_form.save()

        return redirect('teacher_home')
    else:
        assignment_form = CreateAssignmentForm()
    return render(request, 'add_assignment.html', {
        'assignment_form': assignment_form})


def add_rubrik(request, pk):
    assignment = Assignment.objects.get(id=pk)

    if request.method == 'POST':
        form = CreateRubrikForm(request.POST)

        if form.is_valid():
            rubrik = form.save(commit=False)
            rubrik.assignment = assignment
            rubrik.save()
            return redirect('teacher_assignment_view', pk=pk)
    else:
        form = CreateRubrikForm()
    return render(request, 'add_rubrik.html', context={
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
                sub = Submission.objects.get(
                    student__id=s.id, assignment_id=a.id, is_original = True)
                if sub.published_date <= a.submission_date:
                    cell_content = 'on time'
                else:
                    cell_content = 'late'
            except Submission.DoesNotExist:
                cell_content = ''

            row_content.append(cell_content)
        table_content.append(row_content)

    return render(request, 'teacher_home.html', context={'table_content': table_content,
                                                         'assignments': assignments,
                                                         'students': students
                                                         })


def teacher_assignment_view(request, pk):
    assignment = Assignment.objects.get(id=pk)
    try:
        peer_rubrik = Peer_review_rubrik.objects.filter(assignment=pk)
    except Peer_review_rubrik.DoesNotExist:
        peer_rubrik = None

    return render(request, 'teacher_assignment_view.html', context={
        'assignment': assignment,
        'peer_rubrik': peer_rubrik

    })


def teacher_patches(request):
    return render(request, 'teacher_patches.html')


def make_submission(request, pk):
    if request.method == 'POST':
        form = SubmissionForm(request.POST)

        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = Student.objects.get(user=request.user)
            submission.assignment = Assignment.objects.get(id=pk)
            submission.published_date = datetime.now()
            submission.is_original = True
            submission.save()
            return redirect('assignment_view', pk=pk)

        else:
            print(form.errors)
    else:
        form = SubmissionForm()

    return render(request, 'make_submission.html', context={'form': form})


def edit_submission(request, pk):
    assignment = Assignment.objects.get(pk = pk)

    latest_submission, created = Submission.objects.get_or_create(
        assignment=assignment, student=Student.objects.get(user=request.user), is_original = False)
    
    if created:
   
        old_content = Submission.objects.get(assignment=assignment, student=Student.objects.get(user=request.user), is_original = True)
        
        latest_submission.content = old_content.content
    if request.method == 'POST':
        form = EditSubmissionForm(request.POST)
        if form.is_valid():
            updated_submission = form.cleaned_data['content']

            text1 = latest_submission.content
            text2 = updated_submission

            dmp = diff_match_patch()
            diffs = dmp.diff_main(text1,text2)
           
            #text = dmp.patch_toText(diffs)

            


             
            html = dmp.diff_prettyHtml(diffs)

            
            #array = text.split(")(")
            text_string = ""
            
            
            # for a in array:
            #     if a.startswith("("):
            #         a = a.replace("(","", 1)
                    
               
            #     if a.startswith("0"):
            #         text_string+=a
                    
                  
            #     elif a.startswith("1"):
            #         text_string += "\n" + "+++ " + a
                   

            #     elif a.startswith("-1"):
            #         text_string += a + '\u0336'
            print(html)

          
                 

                

            #text_1 = latest_submission.content.split(".")
            #text_2 = updated_submission.split(".")
            #is_added = False
            #string_deleted = ''
            #string_added = ''
            #lib = difflib.Differ()
            #comparing = lib.compare(text_1,text_2)
            #for line in comparing:
             #   print(line)
              #  if line.startswith('+'):
               #    string_added += line + '\n'
               # elif line.startswith('-'):
                #    string_deleted += line + '\n'
                
            
            #submission_edits = Submission_edits(
            #    deleted = diff, added = patches, date_time=datetime.now(), submission=latest_submission)
            #submission_edits.save()
            #latest_submission.content = updated_submission
            #latest_submission.published_date = datetime.now()
            #latest_submission.save()
            return redirect('view_feedback', pk=pk)

    else:
        form = EditSubmissionForm(
            initial={'content': latest_submission.content})

    return render(request, 'edit_submission.html', context={
        'form': form,
        'latest_submission': latest_submission,
        'assignment': assignment
    })


def assignment_view(request, pk):
    assignment = Assignment.objects.get(pk=pk)

    try:
        submission = Submission.objects.get(assignment = assignment, student__user=request.user, is_original = True)
    except Submission.DoesNotExist:
        submission = None

    

    return render(request, 'assignment_view.html', context={
        'assignment': assignment,
        'submission': submission})


def final_assignment_view(request):
    assignment = Assignment.objects.get(is_final=True)
    submissions = Submission.objects.filter(
        is_original=False, student=Student.objects.get(user=request.user))
    return render(request, 'final_assignment_view.html', context={
        'assignment': assignment,
        'submissions': submissions
    })


def give_feedback(request, pk):
    user = Student.objects.get(user=request.user)
    own_group = user.group
    group_members = Student.objects.filter(
        group=own_group).exclude(user=request.user)

    assignment = Assignment.objects.get(id=pk)

    submissions = Submission.objects.filter(
        assignment__id=pk, student__in=group_members)
    print(submissions)
    return render(request, 'give_feedback.html', context={
        'submissions': submissions,
        'assignment': assignment


    })


def group_submission(request, pk, subid):
    print(request.user)
    assignment = Assignment.objects.get(pk=pk)
    submission = Submission.objects.get(id=subid)
    print(submission)
    author = request.user

    peer_review = Feedback.objects.filter(author=author, submission=submission)
    peer_review_id = peer_review.values('peer_review_rubrik')
    peer_rubrik = Peer_review_rubrik.objects.filter(
        assignment=assignment).exclude(id__in=peer_review_id)
    print(peer_review_id)

    form = PeerReviewForm()

    return render(request, 'group_submission.html', context={
        'assignment': assignment,
        'submission': submission,
        'peer_rubrik': peer_rubrik,
        'peer_review': peer_review,
        'form': form
    })


def submit_peer_review(request, pk, subid, rubrik):
    submission = Submission.objects.get(id=subid)
    author = request.user
    peer_rubrik = Peer_review_rubrik.objects.get(id=rubrik)
    form = PeerReviewForm(request.POST)

    if form.is_valid():
        peer_review = form.save(commit=False)
        peer_review.submission = submission
        peer_review.author = author
        peer_review.date = datetime.now()
        peer_review.peer_review_rubrik = peer_rubrik
        peer_review.save()
    return redirect('group_submission', pk=pk, subid=subid)


def view_feedback(request, pk):
   
    submission = Submission.objects.filter(
        assignment=pk, student=Student.objects.get(user=request.user)).latest('id')
    
    assignment = submission.assignment
    peer_reviews = Feedback.objects.filter(
        submission=submission, author__is_student=True).order_by('peer_review_rubrik')
    teacher_feedback = Feedback.objects.filter(
        submission=submission, author__is_teacher=True)
    return render(request, 'view_feedback.html', context={
        'submission': submission,
        'assignment': assignment,
        'peer_reviews': peer_reviews,
        'teacher_feedback': teacher_feedback
    })


def student_home(request):
    assignments = Assignment.objects.filter(is_final=False)
    final_assignment = Assignment.objects.get(is_final=True)
    return render(request, 'student_home.html', context={
        'assignments': assignments,
        'final_assignment': final_assignment})


def stitch_patches(request):
    submission_ids = [int(k) for k in request.POST.keys() if k != 'csrfmiddlewaretoken']
    latest_submissions = Submission.objects.filter(id__in=submission_ids)
    assignments = latest_submissions.values('assignment')
    original_submissions = Submission.objects.filter(student__user = request.user, assignment__in = assignments, is_original = True)
   
    submissions =  zip(original_submissions, latest_submissions)
    submission_edits = Submission_edits.objects.filter(submission__id__in=submission_ids)
   
    
    return render(request, 'stitch_patches.html', context={
        'submissions': submissions,
        'submission_edits': submission_edits})




#Function that initiates a new judgement session.
def new_judge_session(request, pk):
    assignment = Assignment.objects.get(id = pk)
    first_round = Round.objects.create(assignment = assignment, what_round = 1)
    submissions = Submission.objects.filter(assignment__id = pk, is_original = True)
    for s in submissions:
        Script.objects.create(script = s)
    
    scripts = Script.objects.filter(script__in = submissions).order_by('score')
    user = request.user
    return setup_round(pk, scripts, user)



def setup_round(pk, scripts, user):
    what_round = Round.objects.filter(assignment__id = pk).latest('id')
    assignment = Assignment.objects.get(id = pk)
    try:
        iterator = iter(scripts)
        for i in iterator:
                Judgement.objects.create(assignment = assignment, what_round = what_round, judge = user, date_time = datetime.now(), script_a = i, script_b = next(iterator))
    except StopIteration:       
        
            duplicate_script = Script.objects.filter(id__in = scripts).order_by('-score')[1]
            odd_script = Script.objects.latest('id')
            last_judgement = Judgement.objects.create(assignment = assignment, what_round = what_round, judge = user, date_time = datetime.now(), script_a = odd_script, script_b = duplicate_script)
        
     
    
    next_pair = Judgement.objects.filter(what_round = what_round)[0]
    pair_id = next_pair.id

    return redirect('generate_pair', pk=pk, pair_id = pair_id, winner = 0)
 

def generate_pair(request, pk, pair_id, winner):
    
    current_pair = Judgement.objects.get(id = pair_id)
    this_round = current_pair.what_round
    if winner != 0:
        this_winner = Script.objects.get(id = winner)
        current_pair.winner = this_winner
        current_pair.save()
        pairs = Judgement.objects.filter(assignment__id = pk,what_round = this_round, winner__isnull = True)
       
        if pairs:
            next_pair = pairs.first()
            new_score = this_winner.score
            new_score += 1
            this_winner.score =  new_score
            this_winner.save()
        else:
            print(Script.objects.all().count())
            current_pair.winner = None if (Script.objects.all().count()%2 != 0 and this_winner == current_pair.script_b) else this_winner

            if current_pair.winner == this_winner:
                new_score = this_winner.score
                new_score += 1
                this_winner.score =  new_score
                this_winner.save()
            user = request.user
            return evaluate_round(pk, user)
    
    else:

        next_pair = current_pair

    
    return render(request, 'acj_view.html', context = { 'next_pair' : next_pair})




def evaluate_round(pk, user):
    previous_round = Round.objects.filter(assignment__id = pk).latest('id')
    scripts = Script.objects.filter(script__assignment__id = pk).order_by('-score')
    assignment = Assignment.objects.get(id = pk)
    if previous_round.what_round < 5:
        values_list = []

        for s in scripts:
            values_list.append(update_values(pk, s))
           
        i = 0
        for s in scripts:
            s.value = values_list[i]
            s.save()
            i+=1

        scripts = scripts.order_by('-value')

    new_round = previous_round.what_round + 1
    Round.objects.create(assignment = assignment, what_round = new_round)

    return setup_round(pk, scripts, user)





    
    






        


        
        
        



