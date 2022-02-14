from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from pages.models import (Student, User, Lecturer)


class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    contact = forms.CharField(max_length=11)
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['username', 'email', 'contact', 'password1', 'password2', 'captcha']

    def __init__(self, *args, **kwargs):
        super(StudentRegistrationForm, self).__init__(*args, **kwargs)

        for fieldnames in ['username', 'email', 'contact', 'password1', 'password2', 'captcha']:
            self.fields[fieldnames].help_text = None

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        Student.objects.create(user=user)
        return user


class LecturerRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    contact = forms.CharField(max_length=11)

    class Meta:
        model = User
        fields = ['username', 'email', 'contact', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(LecturerRegistrationForm, self).__init__(*args, **kwargs)

        for fieldnames in ['username', 'email', 'contact', 'password1', 'password2']:
            self.fields[fieldnames].help_text = None

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_lecturer = True
        user.save()
        Lecturer.objects.create(user=user)
        return user
