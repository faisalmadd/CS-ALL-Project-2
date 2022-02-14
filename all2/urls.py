"""all2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from pages.views import homepage_view, contact_view, StudentRegisterView, profile_view, admin_dashboard, \
    student_dashboard, lecturer_dashboard, login_view, login_form, admin_add_student, LecturerRegisterView
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', homepage_view, name='home'),  # 1st arg '' means Home Page
    path('contact/', contact_view, name='contact'),
    path('register/', StudentRegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('login_form/', login_form, name='login_form'),
    path('logout/', auth_view.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),

    # admin pages
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin_add_lecturer/', LecturerRegisterView.as_view(), name='admin_add_lecturer'),
    path('admin_add_student/', admin_add_student, name='admin_add_student'),

    # lecturer pages
    path('lecturer/dashboard/', lecturer_dashboard, name='lecturer_dashboard'),

    # student pages
    path('student/dashboard/', student_dashboard, name='student_dashboard'),

]
