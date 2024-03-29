from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import UserRegisterForm, UserEditForm
from .models import User

from . import models


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'patch', 'student', 'content')

class Submission_editsAdmin(admin.ModelAdmin):
    list_display = ('id', 'submission', 'date_time')

class ScriptAdmin(admin.ModelAdmin):
    list_display = ('id', 'score', 'value')


admin.site.register(models.Submission, SubmissionAdmin)
admin.site.register(models.User)
admin.site.register(models.Patch)
admin.site.register(models.Student)
admin.site.register(models.Peer_review_rubrik)
admin.site.register(models.Feedback)
admin.site.register(models.Submission_edits, Submission_editsAdmin)
admin.site.register(models.Script, ScriptAdmin)
admin.site.register(models.Judgement)
admin.site.register(models.Round)
