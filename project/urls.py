from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('teacher_register', views.teacher_register, name='teacher_register'),
    path('student_home', views.student_home, name = 'student_home'),
    path('patch/', views.patch, name='patch'),
    path('patch/assessment/', views.assessment, name='assessment'),
    path('patch/give_feedback/', views.give_feedback, name='give_feedback'),
    path('patch/view_feedback/', views.view_feedback, name='view_feedback'),
    path('patch/assessment/make_submission', views.make_submission, name='make_submission'),
    path('teacher_home', views.teacher_home, name='teacher_home'),
    path('teacher_home/teacher_patches', views.teacher_patches, name='teacher_patches'),
    path('teacher_home/add_student', views.add_student, name = 'add_student')
]
