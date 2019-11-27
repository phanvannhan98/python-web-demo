"""Defines URL pattern for application Polls"""
from django.urls import path
from . import views

#name space help distinguish this urls.py from files in other apps
app_name = 'polls'

urlpatterns=[
    # Home page
    path('', views.index, name='index'),
    # Page that shows all question
    path('questions/', views.questions, name='questions'),
    path('questions/<int:question_id>', views.question, name='question'),
    path('new_question/', views.new_question, name='new_question'),
    path('new_choice/<int:question_id>', views.new_choice, name='new_choice'),
]
