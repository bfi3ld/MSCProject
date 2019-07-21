from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
import django.utils.timezone

# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 30, unique = True)

    def _str_(self):
        return self.name




    
class Patch(models.Model):
    number = models.IntegerField(unique = True)
    start_date = models.DateField()
    end_date = models.DateField()
    submission_date = models.DateField()
    peer_review_end_date = models.DateField()
    submission_open = models.BooleanField()
    peer_review_open = models.BooleanField()

class Assessment(models.Model):
    
    title = models.CharField(max_length = 100)
    description = models.TextField()



class Submission(models.Model):
    #patch = models.ForeignKey('Patch', on_delete=models.CASCADE)
    #title = models.ForeignKey('Assessment', on_delete=models.CASCADE)
    content = HTMLField('content', default = "")
    published_date = models.DateTimeField(blank = True, null=True)
    #student = models.ForeignKey('Student', on_delete=models.CASCADE)

   



class Peer_review_rubrik(models.Model):
    instruction = models.TextField()
    assessment = models.ForeignKey('Assessment', on_delete = models.CASCADE)


class Peer_review_submission(models.Model):
    peer_review_rubrik = models.ForeignKey('Peer_review_rubrik', on_delete=models.CASCADE)
    submission = models.ForeignKey('Submission', on_delete = models.CASCADE)
    review = models.TextField()
    author = models.ForeignKey('Student', on_delete = models.CASCADE)
    date = models.DateField()










    







