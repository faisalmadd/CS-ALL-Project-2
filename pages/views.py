from django.contrib.auth import login, authenticate
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Count
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DeleteView
from .models import TakenQuiz, Profile, Quiz, Question, Answer, Student, User, Course, Tutorial, Notes, Announcement
from .forms import StudentRegistrationForm, LecturerRegistrationForm, AdminStudentRegistrationForm, QuestionForm, \
    BaseAnswerInlineFormSet


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
        return redirect('lecturer_dashboard')


class AdminStudentRegisterView(CreateView):
    model = User
    form_class = AdminStudentRegistrationForm
    template_name = 'dashboard/admin/add_student.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        # return redirect('learner')
        return redirect('student_dashboard')


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


def add_course(request):
    if request.method == 'POST':
        name = request.POST['name']

        a = Course(name=name)
        a.save()
        messages.success(request, 'Successfully Added Course')
        return redirect('add_course')
    else:
        return render(request, 'dashboard/lecturer/add_course.html')


class ManageUserView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'dashboard/admin/manage_users.html'
    context_object_name = 'users'
    paginated_by = 10

    def get_queryset(self):
        return User.objects.order_by('-id')


class DeleteUser(SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'dashboard/admin/delete_user.html'
    success_url = reverse_lazy('manage_users')
    success_message = 'User was deleted successfully!'


class AddQuizView(CreateView):
    model = Quiz
    fields = ('name', 'course')
    template_name = 'dashboard/lecturer/add_quiz.html'

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.owner = self.request.user
        quiz.save()
        messages.success(self.request, 'Quiz created')
        return redirect('update_quiz', quiz.pk)


class UpdateQuizView(CreateView):
    model = Quiz
    fields = ('name', 'course')
    template_name = 'dashboard/lecturer/update_quiz.html'

    def get_context_data(self, **kwargs):
        kwargs['questions'] = self.get_object().questions.annotate(answers_count=Count('answers'))
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()

    def get_success_url(self):
        return reverse('update_quiz', kwargs={'pk', self.object.pk})


def add_question(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, 'Please add answers to the questions')
            return redirect('question_change', quiz.pk, question.pk)
        else:
            form = QuestionForm()

        return render(request, 'dashboard/lecturer/add_question.html', {'quiz': quiz, 'form': form})


def update_question(request, quiz_pk, question_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk, owner=request.user)
    question = get_object_or_404(Question, pk=question_pk, quiz=quiz)

    AnswerFormatSet = inlineformset_factory(
        Question,
        Answer,
        formset=BaseAnswerInlineFormSet,
        fields=('text', 'is_correct'),
        min_num=2,
        validate_min=True,
        max_num=10,
        validate_max=True
    )

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormatSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                formset.save()
                formset.save()
            messages.success(request, 'Question And Answers Saved Successfully')
            return redirect('quiz_change', quiz.pk)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormatSet(instance=question)
    return render(request, 'dashboard/lecturer/update_questions.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'formset': formset
    })


class QuizListView(ListView):
    model = Quiz
    ordering = ('name',)
    context_object_name = 'quizzes'
    template_name = 'dashboard/lecturer/update_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.quizzes \
            .select_related('course') \
            .annotate(questions_count=Count('questions', distinct=True)) \
            .annotate(taken_count=Count('taken_quizzes', distinct=True))
        return queryset
