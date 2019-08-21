from django.db import models
from django.contrib.auth.models import AbstractUser
from tinymce.models import HTMLField

import django.utils.timezone


class User(AbstractUser):
    email = models.CharField(max_length=100, default='')
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.IntegerField()


class Patch(models.Model):
    patch_title = models.CharField(max_length=100, default='')
    patch_description = models.TextField()
    submission_date = models.DateTimeField(null=True)
    peer_review_date = models.DateTimeField(null=True)
    is_final = models.BooleanField(default=False)


class Submission(models.Model):
    patch = models.ForeignKey(Patch, on_delete=models.CASCADE)
    content = HTMLField('content')  
    published_date = models.DateTimeField(blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_original = models.BooleanField(default=False)


class Submission_edits(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    deleted = models.TextField(null = True)
    added = models.TextField(null = True)
    date_time = models.DateTimeField()


class Peer_review_rubrik(models.Model):
    instruction = models.TextField()
    patch = models.ForeignKey(Patch, on_delete=models.CASCADE)


class Feedback(models.Model):
    peer_review_rubrik = models.ForeignKey(
        'Peer_review_rubrik', on_delete=models.CASCADE, null=True)
    submission = models.ForeignKey('Submission', on_delete=models.CASCADE)
    review = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

#Script b is set to null=True so one duplicate script can be added after object is created, if the scripts are
#odd numbered.
class Judgement(models.Model):
    patch = models.ForeignKey('Patch', on_delete = models.CASCADE)
    script_a = models.ForeignKey('Script', related_name = 'script_a', on_delete = models.CASCADE)
    script_b = models.ForeignKey('Script',related_name = 'script_b', on_delete = models.CASCADE, null = True)
    winner = models.ForeignKey('Script', on_delete = models.CASCADE, null = True)
    what_round = models.ForeignKey('Round', on_delete = models.CASCADE)
    judge = models.ForeignKey('User', on_delete = models.CASCADE)
    date_time = models.DateTimeField()


class Script(models.Model):
    script = models.OneToOneField('Submission', on_delete = models.CASCADE)
    score = models.IntegerField(default = '0')
    value = models.DecimalField(default = '1.0', max_digits= 100, decimal_places = 5)

    

class Round(models.Model):
    patch = models.ForeignKey('Patch', on_delete = models.CASCADE)
    what_round = models.IntegerField(null = True)
    reliability = models.IntegerField(null = True)


