from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('patch/', views.patch, name='patch'),
    path('patch/assessment/', views.assessment, name='assessment'),
    path('patch/give_feedback/', views.give_feedback, name='give_feedback'),
    path('patch/view_feedback/', views.view_feedback, name='view_feedback'),
    path('patch/assessment/make_submission', views.make_submission, name = 'make_submission')
]