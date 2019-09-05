from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.timezone import datetime
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from project.acj import estimate_values
from project.forms import *
from project.models import *

from diff_match_patch import diff_match_patch
from bs4 import BeautifulSoup

"""Function that controls user permission. It is being used as a decorator in the 
    other functions in this file that have restricted access based on user type."""
def project_login_required(user_allowed):
    def wrap(function):
        def wrapper(request, *args, **kw):
            user = request.user
            if user.is_authenticated and (
                    (user_allowed == 'teacher' and user.is_teacher) or \
                    (user_allowed == 'student' and user.is_student)):
                return function(request, *args, **kw)
            else:
                return redirect('index')

        return wrapper

    return wrap

"""Function that returns the index-page, where the login/register option is."""
def index(request):
    return render(request, 'index.html')


"""Function that lets a teacher register and creates a teacher-user object."""
def teacher_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_teacher = True
            user.save()

            return redirect('index')
    else:

        form = UserRegisterForm()
    return render(request, 'teacher_register.html', {'form': form})


"""Function that handles the login-functionality. The validation of user credentials is handled by Django's own authentication-system."""
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

"""Function that handles the logout of a user. Uses the Djangos authentication system to achieve this."""
def log_out(request):
    logout(request)
    return redirect('index')

""""Function that creates a student-user object. Uses the project_login_required decorator to ensure only authorised access."""
@project_login_required(user_allowed='teacher')
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


""""Function that creates a patch-object. Uses the project_login_required decorator to ensure only authorised access."""
@project_login_required(user_allowed='teacher')
def add_patch(request):
    if request.method == 'POST':
        patch_form = CreatePatchForm(request.POST)
        if patch_form.is_valid():
            patch_form.save()
            quilt, created = Patch.objects.get_or_create(
                is_final=True)
            if created:
                quilt.patch_title = "Final patch"
                quilt.patch_description = "final patch"
                quilt.save()

        return redirect('teacher_home')
    else:
        patch_form = CreatePatchForm()
    return render(request, 'add_patch.html', {
        'patch_form': patch_form})

""""Function that creates a peer-rubric object. Uses the project_login_required decorator to ensure only authorised access."""
@project_login_required(user_allowed='teacher')
def add_rubric(request, pk):
    patch = Patch.objects.get(id=pk)

    if request.method == 'POST':
        form = CreateRubrikForm(request.POST)

        if form.is_valid():
            rubrik = form.save(commit=False)
            rubrik.patch = patch
            rubrik.save()
            return redirect('teacher_patch_view', pk=pk)
    else:
        form = CreateRubrikForm()
    return render(request, 'add_rubrik.html', context={
        'form': form,
    })


"""Function that renders the teacher home-page. It gets all the data regarding the patches, students, their
    submissions and editing, and adds it to a 3d array, so it can be easily displayed in a table in the template. """
@project_login_required(user_allowed='teacher')
def teacher_home(request):
    students = Student.objects.all()
    patches = Patch.objects.filter(is_final=False)
    final_quilt = Patch.objects.get(is_final=True)
    submissions = Submission.objects.all().order_by('student', 'patch')  
    sub_edits = Submission.objects.all()

    arr = []
    for student in students:
        sub_arr = []

        for patch in patches:
            sub_sub_arr = []
            sub = '&#10006'
            edit_count = 0
            reviewed = '&#10006'

            #Checking if the students have submitted in time or not.
            try:
                org_sub = Submission.objects.get(student=student, patch=patch, is_original=True)
                if org_sub.published_date < org_sub.patch.submission_date:
                    sub = '&#10004;'
                else:
                    sub = '!'

                #Checking if the student have completed the all the required peer-reviewing.
                peer_review = Feedback.objects.filter(author=student.user, submission__patch=patch).values(
                    'submission').distinct()
                no_of_reviews_needed = Student.objects.filter(group=student.group).count() - 1
                
                if peer_review.count() == no_of_reviews_needed:
                     reviewed =  "&#10004;"
                
                #Checks how many times a student has edited a submission.
                edited_sub = Submission.objects.filter(student=student, patch=patch, is_original=False)
                if edited_sub:
                    edit_count = Submission_edits.objects.filter(submission__in=edited_sub).count()

            except org_sub.DoesNotExist:
                pass

            sub_sub_arr.append(sub)
            sub_sub_arr.append(reviewed)
            sub_sub_arr.append(edit_count)
            sub_arr.append(sub_sub_arr)

        arr.append(sub_arr)
        zipped = zip(students, arr)

    return render(request, 'teacher_home.html', context={
        'patches': patches,
        'final_quilt': final_quilt,
        'students': students,
        'submissions': submissions,
        'sub_edits': sub_edits,
        'arr': arr,
        'zipped': zipped
    })

"""Function that renders the teachers patch-view"""
@project_login_required(user_allowed='teacher')
def teacher_patch_view(request, pk):
    patch = Patch.objects.get(id=pk)
    try:
        peer_rubrik = Peer_review_rubrik.objects.filter(patch=pk)
    except Peer_review_rubrik.DoesNotExist:
        peer_rubrik = None

    return render(request, 'teacher_patch_view.html', context={
        'patch': patch,
        'peer_rubrik': peer_rubrik

    })




@project_login_required(user_allowed='student')
def make_submission(request, pk):
    if request.method == 'POST':
        form = SubmissionForm(request.POST)

        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = Student.objects.get(user=request.user)
            submission.patch = Patch.objects.get(id=pk)
            submission.published_date = datetime.now()
            submission.is_original = True
            submission.save()
            return redirect('patch_view', pk=pk)

        else:
            print(form.errors)
    else:
        form = SubmissionForm()

    return render(request, 'make_submission.html', context={'form': form})


@project_login_required(user_allowed='student')
def edit_submission(request, pk):
    patch = Patch.objects.get(pk=pk)
    display_html = ''

    latest_submission, created = Submission.objects.get_or_create(
        patch=patch, student=Student.objects.get(user=request.user), is_original=False)

    if created:
        old_content = Submission.objects.get(patch=patch, student=Student.objects.get(user=request.user),
                                             is_original=True)

        latest_submission.content = old_content.content
        latest_submission.save()
    if request.method == 'POST':
        form = EditSubmissionForm(request.POST)
        if form.is_valid():
            updated_submission = form.cleaned_data['content']

            text1 = BeautifulSoup(latest_submission.content, features="html.parser")
            text2 = BeautifulSoup(updated_submission, features="html.parser")

            conv_1 = text1.get_text()
            conv_2 = text2.get_text()

            dmp = diff_match_patch()
            difference = dmp.diff_main(conv_1, conv_2)

            dmp.diff_cleanupSemantic(difference)

            display_html = dmp.diff_prettyHtml(difference)

            latest_submission.content = updated_submission
            latest_submission.published_date = datetime.now()
            latest_submission.save()

            submission_edits = Submission_edits(
                deleted=display_html, date_time=datetime.now(), submission=latest_submission)
            submission_edits.save()
            latest_submission.content = updated_submission
            latest_submission.published_date = datetime.now()
            latest_submission.save()
            return redirect('view_feedback', pk=pk)

    else:
        form = EditSubmissionForm(
            initial={'content': latest_submission.content})

    return render(request, 'edit_submission.html', context={
        'form': form,
        'latest_submission': latest_submission,
        'patch': patch,
        'display_html': display_html
    })


@project_login_required(user_allowed='student')
def patch_view(request, pk):
    patch = Patch.objects.get(pk=pk)

    try:
        submission = Submission.objects.get(patch=patch, student__user=request.user, is_original=True)
    except Submission.DoesNotExist:
        submission = None

    return render(request, 'patch_view.html', context={
        'patch': patch,
        'submission': submission})


@login_required()
def final_patch_view(request, student_id):
    patch = Patch.objects.get(is_final=True)
    student= Student.objects.get(id = student_id)
    submissions = Submission.objects.filter(
        student=student, is_original=True)

    return render(request, 'final_patch_view.html', context={
        'patch': patch,
        'submissions': submissions,
        'student':student
    })


@project_login_required(user_allowed='student')
def give_feedback(request, pk):
    user = Student.objects.get(user=request.user)
    own_group = user.group
    group_members = Student.objects.filter(
        group=own_group).exclude(user=request.user)

    patch = Patch.objects.get(id=pk)

    submission = Submission.objects.filter(
        patch__id=pk, student__in=group_members, is_original=True)
   
    return render(request, 'give_feedback.html', context={
        'submission': submission,
        'patch': patch

    })


@project_login_required(user_allowed='student')
def group_submission(request, pk, subid):
    patch = Patch.objects.get(pk=pk)
    submission = Submission.objects.get(id=subid)

    author = request.user

    peer_review = Feedback.objects.filter(author=author, submission=submission)
    peer_review_id = peer_review.values('peer_review_rubrik')
    peer_rubrik = Peer_review_rubrik.objects.filter(
        patch=patch).exclude(id__in=peer_review_id)
   

    form = PeerReviewForm()

    return render(request, 'group_submission.html', context={
        'patch': patch,
        'submission': submission,
        'peer_rubrik': peer_rubrik,
        'peer_review': peer_review,
        'form': form
    })


@project_login_required(user_allowed='student')
def submit_peer_review(request, pk, subid, rubrik):
    submission = Submission.objects.get(id=subid)
    author = request.user
    peer_rubrik = Peer_review_rubrik.objects.get(id=rubrik)
    form = PeerReviewForm()

    if request == POST:
        if form.is_valid():
        
        form = PeerReviewForm(request.POST)
        peer_review = form.save(commit=False)
        peer_review.submission = submission
        peer_review.author = author
        peer_review.date = datetime.now()
        peer_review.peer_review_rubrik = peer_rubrik
        peer_review.save()
        
    return redirect('group_submission', pk=pk, subid=subid)


@project_login_required(user_allowed='student')
def view_feedback(request, pk):
    student = Student.objects.get(user=request.user)
    submission = Submission()
    patch = Patch.objects.get(id=pk)
    try:
        submission = Submission.objects.filter(
            patch=pk, student=Student.objects.get(user=request.user)).latest('id')

    except submission.DoesNotExist:
        pass

    peer_reviews = Feedback.objects.filter(
        submission__in = Submission.objects.filter(patch=pk, student=Student.objects.get(user=request.user)), author__is_student=True).order_by('peer_review_rubrik')
    teacher_feedback = Feedback.objects.filter(
        submission=submission, author__is_teacher=True)
    return render(request, 'view_feedback.html', context={
        'submission': submission,
        'patch': patch,
        'peer_reviews': peer_reviews,
        'teacher_feedback': teacher_feedback
    })


@project_login_required(user_allowed='student')
def student_home(request):
    patches = Patch.objects.filter(is_final=False)
    final_patch = Patch.objects.get(is_final=True)
    student= Student.objects.get(user = request.user)
    student_id = student.id
    return render(request, 'student_home.html', context={
        'patches': patches,
        'final_patch': final_patch,
        'student_id':student_id
        })


@login_required()
def stitch_patches(request, student_id):
    

    patch_ids = [int(k) for k in request.POST.keys() if k != 'csrfmiddlewaretoken']
    patches = Patch.objects.filter(id__in=patch_ids)
    student = Student.objects.get(id = student_id)



    original_submissions = Submission.objects.filter(student__id = student_id, patch__id__in=patches,
                                                     is_original=True).order_by('patch__id')

                                                  
    latest_submissions = Submission.objects.filter(student__id = student_id, patch__id__in=patches, is_original=False)

    
     
    submission_edits = Submission_edits.objects.filter(submission__id__in=latest_submissions)
    feedback = Feedback.objects.filter(submission__in=original_submissions)
    print(feedback)

    return render(request, 'stitch_patches.html', context={
        'original':original_submissions,
        'latest':latest_submissions,
        'submission_edits': submission_edits,
        'feedback': feedback})


def teacher_feedback(request, sub_id):

    submission = Submission.objects.get(id = sub_id)
    form = PeerReviewForm()
    if request.method == 'POST':
        
        form = PeerReviewForm(request.POST)
        
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.author = request.user
            feedback.submission = submission
            feedback.date = datetime.now()
            feedback.save()
            return redirect('teacher_home')

   
    return render(request, 'teacher_feedback.html', context={
        'form':form,
        'submission':submission
    })

@project_login_required(user_allowed='teacher')
def new_judge_session(request, pk):
    """Function that initiates a new judgement session."""
    patch = Patch.objects.get(id=pk)
    first_round = Round.objects.create(patch=patch, what_round=1)
    submissions = Submission.objects.filter(patch__id=pk, is_original=True)
    for s in submissions:
        Script.objects.create(script=s)

    scripts = Script.objects.filter(script__in=submissions).order_by('score')
    user = request.user
    return setup_round(pk, scripts, user)


def setup_round(pk, scripts, user):
    """Function that sets up each round by creating the judgement objects and assign pairs."""
    what_round = Round.objects.filter(patch__id=pk).latest('id')
    patch = Patch.objects.get(id=pk)
    try:
        iterator = iter(scripts)
        for i in iterator:
            Judgement.objects.create(patch=patch, what_round=what_round, judge=user, date_time=datetime.now(),
                                     script_a=i, script_b=next(iterator))
    except StopIteration:
        # If there are an odd number of scripts the last script will be compared to the one before it,
        # but if the duplicate one wins it will not get a score. 
        duplicate_script = Script.objects.filter(id__in=scripts).order_by('-score')[1]
        odd_script = Script.objects.latest('id')
        last_judgement = Judgement.objects.create(patch=patch, what_round=what_round, judge=user,
                                                  date_time=datetime.now(), script_a=odd_script,
                                                  script_b=duplicate_script)

    next_pair = Judgement.objects.filter(what_round=what_round)[0]
    pair_id = next_pair.id

    return redirect('generate_pair', pk=pk, pair_id=pair_id, winner=0)


@project_login_required(user_allowed='teacher')
def generate_pair(request, pk, pair_id, winner):
    current_pair = Judgement.objects.get(id=pair_id)
    this_round = current_pair.what_round

    # if first judgment of the round
    if winner == 0: return render(request, 'acj_view.html', context={'next_pair': current_pair})

    this_winner = Script.objects.get(id=winner)
    this_winner.score += 1
    this_winner.save()

    current_pair.winner = this_winner
    current_pair.save()

    pairs = Judgement.objects.filter(patch__id=pk, what_round=this_round, winner__isnull=True)

    if pairs:
        next_pair = pairs.first()
    else:

        user = request.user
        return evaluate_round(pk, user)

    return render(request, 'acj_view.html', context={'next_pair': next_pair})


def evaluate_round(pk, user):
    previous_round = Round.objects.filter(patch__id=pk).latest('id')
    scripts = Script.objects.filter(script__patch__id=pk).order_by('-score')
    patch = Patch.objects.get(id=pk)
    if previous_round.what_round > 4:
        scores = [float(s.score) for s in scripts]
        values = [float(s.value) for s in scripts]
        vals, _ = estimate_values(scores, vals=values)

        for script, val in zip(scripts, vals):
            script.value = val
            script.save()

    scripts = scripts.order_by('-value')

    new_round = previous_round.what_round + 1
    Round.objects.create(patch=patch, what_round=new_round)

    return setup_round(pk, scripts, user)
