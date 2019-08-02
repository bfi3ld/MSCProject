from django.db import models
from django.contrib.auth.models import AbstractUser

import django.utils.timezone

# Create your models here.


class User(AbstractUser):
    email = models.CharField(max_length =100, default = '') 
    is_teacher = models.BooleanField(default = False)
    is_student = models.BooleanField(default = False)
    

class Student(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    group = models.IntegerField()


class Assignment(models.Model):
    assignment_title = models.CharField(max_length=100, default = '')
    assignment_description = models.TextField()
    submission_date = models.DateTimeField()
    peer_review_date = models.DateTimeField()

    
    


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    content = models.TextField()  # ('content', default = "")
    published_date = models.DateTimeField(blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)



class Peer_review_rubrik(models.Model):
    instruction = models.TextField()
    assignment = models.ForeignKey(Assignment, on_delete = models.CASCADE)


class Peer_review_submission(models.Model):
    peer_review_rubrik = models.ForeignKey('Peer_review_rubrik', on_delete=models.CASCADE, null = True)
    submission = models.ForeignKey('Submission', on_delete = models.CASCADE)
    review = models.TextField()
    author = models.ForeignKey(Student, on_delete = models.CASCADE)
    date = models.DateField()
