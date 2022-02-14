from django.contrib.auth import login, authenticate
from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import CreateView
from .models import TakenQuiz, Profile, Quiz, Question, Answer, Student, User, Course, Tutorial, Notes, Announcement
from .forms import StudentRegistrationForm, LecturerRegistrationForm
from all2 import settings
import requests


# Create your views here.
def homepage_view(request, *args, **kwargs):
    return render(request, "home.html", {})


class StudentRegisterView(CreateView):
    model = User
    form_class = StudentRegistrationForm
    template_name = 'register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        user = form.cleaned_data.get('username')
        messages.success(self.request, f'Hi {user}, your account was created successfully!')
        # return redirect('learner')
        return redirect('home')


class LecturerRegisterView(CreateView):
    model = User
    form_class = LecturerRegistrationForm
    template_name = 'dashboard/admin/add_lecturer.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'lecturer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        user = form.cleaned_data.get('username')
        messages.success(self.request, f'Hi {user}, your account was created successfully!')
        # return redirect('learner')
        return redirect('admin_add_lecturer')


def login_form(request):
    return render(request, 'login.html')


def login_view(request, *args, **kwargs):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_admin or user.is_superuser:
                return redirect('admin_dashboard')
            elif user.is_lecturer:
                return redirect('lecturer_dashboard')
            elif user.is_student:
                return redirect('student_dashboard')
            else:
                return redirect('login_form')
        else:
            messages.info(request, "Invalid Username or Password")
            return redirect('login_form')


def contact_view(request, *args, **kwargs):
    return render(request, "contact.html", {})


def profile_view(request, *args, **kwargs):
    return render(request, "profile.html", {})


def student_dashboard(request, *args, **kwargs):
    return render(request, "dashboard/student/dashboard.html", {})


def lecturer_dashboard(request, *args, **kwargs):
    return render(request, "dashboard/lecturer/dashboard.html", {})


def admin_dashboard(request, *args, **kwargs):
    return render(request, "dashboard/admin/dashboard.html", {})


def admin_add_lecturer(request, *args, **kwargs):
    return render(request, "dashboard/admin/add_lecturer.html", {})


def admin_add_student(request, *args, **kwargs):
    return render(request, "dashboard/admin/add_student.html", {})