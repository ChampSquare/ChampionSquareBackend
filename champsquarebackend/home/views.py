from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
def old_home(request):
    return render(request, 'old/home.html', {})


def index(request):
    return render(request, 'home.html', {})


def view_student(request):
    return render(request, 'student.html', {})


def view_teacher(request):
    return render(request, 'teacher.html', {})


def view_parent(request):
    return render(request, 'parent.html', {})


def view_school(request):
    return render(request, 'school.html', {})