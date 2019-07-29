from django.db import models
from django.contrib.auth.models import AbstractUser

import django.utils.timezone

# Create your models here.


class User(AbstractUser):
    
   
    is_student = models.BooleanField('student', default=False)
    is_teacher = models.BooleanField('teacher', default=False)
    email = models.CharField(max_length =100, default = '') 
    



class Assignment(models.Model):
    assignment_title = models.CharField(max_length=100, primary_key=True)
    assignment_description = models.TextField()
    submission_date = models.DateTimeField()
    peer_review_date = models.DateTimeField()
    
    


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    content = models.TextField()  # ('content', default = "")
    published_date = models.DateTimeField(blank=True, null=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE)


class Peer_rubrik(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
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
