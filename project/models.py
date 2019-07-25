from django.db import models
from django.contrib.auth.models import User

import django.utils.timezone

# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_student = models.BooleanField('student', default=True)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_teacher = models.BooleanField('teacher', default=True)


class Patch(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    start_date = models.DateTimeField()
    submission_date = models.DateTimeField()
    peer_review_date = models.DateTimeField()
    assignment_title = models.CharField(max_length=100)
    assignment_description = models.TextField()


class Submission(models.Model):
    patch = models.ForeignKey(Patch, on_delete=models.CASCADE)
    content = models.TextField()  # ('content', default = "")
    published_date = models.DateTimeField(blank=True, null=True)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)


class Peer_rubrik(models.Model):
    patch = models.ForeignKey(Patch, on_delete=models.CASCADE)
    peer_rubrik_text = models.TextField(default='')

# class Peer_review_rubrik(models.Model):
#     instruction = models.TextField()
#     assessment = models.ForeignKey(Assessment, on_delete = models.CASCADE)


# class Peer_review_submission(models.Model):
#     peer_review_rubrik = models.ForeignKey('Peer_review_rubrik', on_delete=models.CASCADE)
#     submission = models.ForeignKey('Submission', on_delete = models.CASCADE)
#     review = models.TextField()
#     author = models.ForeignKey(User, on_delete = models.CASCADE)
#     date = models.DateField()
