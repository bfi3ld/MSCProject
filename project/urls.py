from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.log_in, name = 'login'),
    path('teacher_register', views.teacher_register, name='teacher_register'),
    path('student_home', views.student_home, name = 'student_home'),
    path('student_home/assignment_view/<int:pk>', views.assignment_view, name = 'assignment_view'),
    path('student_home/assignment_view/<int:pk>/give_feedback', views.give_feedback, name='give_feedback'),
    path('student_home/assignment_view/<int:pk>/give_feedback/group_submission/<int:subid>', views.group_submission, name='group_submission'),
    path('student_home/assignment_view/<int:pk>/give_feedback/group_submission/<int:subid>/submit_peer_review/<int:rubrik>', views.submit_peer_review, name='submit_peer_review'),
    path('student_home/assignment_view/<int:pk>/view_feedback', views.view_feedback, name='view_feedback'),
    path('student_home/assignment_view/<int:pk>/view_feedback/edit_submission', views.edit_submission, name='edit_submission'),
    path('student_home/assignment_view/<int:pk>/make_submission', views.make_submission, name='make_submission'),
    path('student_home/final_assignment_view', views.final_assignment_view, name = 'final_assignment_view'),
    path('student_home/final_assignment_view/stitch_patches', views.stitch_patches, name='stitch_patches'),
    path('teacher_home', views.teacher_home, name='teacher_home'),
    path('teacher_home/teacher_patches', views.teacher_patches, name='teacher_patches'),
    path('teacher_home/teacher_assignment_view/<int:pk>', views.teacher_assignment_view, name = 'teacher_assignment_view'),
    path('teacher_home/teacher_assignment_view/<int:pk>/add_rubrik', views.add_rubrik, name = 'add_rubrik'),
    path('teacher_home/add_student', views.add_student, name = 'add_student'),
    path('teacher_home/add_assignment', views.add_assignment, name = 'add_assignment'),
    path('teacher_home/teacher_assignment_view/<int:pk>/new_judge_session', views.new_judge_session, name = 'new_judge_session'),
    path('teacher_home/teacher_assignment_view/<int:pk>/acj/<int:int_round>', views.generate_pair, name = 'generate_pair')
    
]
