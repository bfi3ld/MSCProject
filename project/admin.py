from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import UserRegisterForm, UserEditForm
from .models import User

from . import models

admin.site.register(models.Submission)
admin.site.register(models.User)
admin.site.register(models.Patch)

