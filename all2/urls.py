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

from django.conf import settings
from django.conf.urls.static import static
from pages.views import homepage_view, contact_view, StudentRegisterView, profile_view, admin_dashboard, \
    student_dashboard, lecturer_dashboard, login_view, login_form, LecturerRegisterView, \
    AdminStudentRegisterView, ManageUserView, DeleteUser, add_course, AddQuizView, UpdateQuizView, add_question, \
    update_question, QuizListView, DeleteQuestion, DeleteQuiz, ResultsView, post_tutorial, LecturerTutorialDetail, \
    list_tutorial, add_tutorial, AddComment
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
    path('admin_add_student/', AdminStudentRegisterView.as_view(), name='admin_add_student'),
    path('manage_users/', ManageUserView.as_view(), name='manage_users'),
    path('delete_user/<int:pk>', DeleteUser.as_view(), name='delete_user'),

    # lecturer pages
    path('lecturer_dashboard/', lecturer_dashboard, name='lecturer_dashboard'),
    path('add_course/', add_course, name='add_course'),
    path('add_quiz/', AddQuizView.as_view(), name='add_quiz'),
    path('list_quiz/', QuizListView.as_view(), name='list_quiz'),
    path('update_quiz/<int:pk>/', UpdateQuizView.as_view(), name='update_quiz'),
    path('add_question/<int:pk>/', add_question, name='add_question'),
    path('quiz/<int:quiz_pk>/<int:question_pk>/', update_question, name='update_questions'),
    path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', DeleteQuestion.as_view(), name='delete_question'),
    path('quiz/<int:pk>/delete/', DeleteQuiz.as_view(), name='delete_quiz'),
    path('quiz/<int:pk>/results/', ResultsView.as_view(), name='quiz_results'),
    path('tutorial/', add_tutorial, name='add_tutorial'),
    path('post/', post_tutorial, name='post_tutorial'),
    path('list_tutorial/', list_tutorial, name='list_tutorial'),
    path('lecturer_tutorials/<int:pk>/', LecturerTutorialDetail.as_view(), name="lecturer_tutorial_detail"),
    path('lecturer_tutorials/<int:pk>/comment', AddComment.as_view(), name="lecturer_add_comment"),

    # student pages
    path('student/dashboard/', student_dashboard, name='student_dashboard'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
