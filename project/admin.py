from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import UserRegisterForm, UserEditForm
from .models import User

from . import models


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'assignment', 'student', 'content')

class Submission_editsAdmin(admin.ModelAdmin):
    list_display = ('id', 'submission', 'date_time')


admin.site.register(models.Submission, SubmissionAdmin)
admin.site.register(models.User)
admin.site.register(models.Assignment)
admin.site.register(models.Student)
admin.site.register(models.Peer_review_rubrik)
admin.site.register(models.Feedback)
admin.site.register(models.Submission_edits, Submission_editsAdmin)
