from django.urls import path

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('student', views.view_student, name="student"),
    path('teacher', views.view_teacher, name="teacher"),
    path('parent', views.view_parent, name="parent"),
    path('school', views.view_school, name="school")
]
