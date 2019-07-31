from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.log_in, name = 'login'),
    path('teacher_register', views.teacher_register, name='teacher_register'),
    path('student_home', views.student_home, name = 'student_home'),
    path('student_home/assignment_view/<int:pk>', views.assignment_view, name = 'assignment_view'),
    path('student_home/assignment_view/<int:pk>/give_feedback', views.give_feedback, name='give_feedback'),
    path('student_home/assignment_view/<int:pk>/give_feedback/group_submission', views.group_submission, name='group_submission'),
    path('student_home/assignment_view/<int:pk>/view_feedback', views.view_feedback, name='view_feedback'),
    path('student_home/assignment_view/<int:pk>/make_submission', views.make_submission, name='make_submission'),
    path('teacher_home', views.teacher_home, name='teacher_home'),
    path('teacher_home/teacher_patches', views.teacher_patches, name='teacher_patches'),
    path('teacher_home/add_student', views.add_student, name = 'add_student'),
    path('teacher_home/add_assignment', views.add_assignment, name = 'add_assignment')
]
