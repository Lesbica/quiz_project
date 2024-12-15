# Імпортуємо необхідні модулі та функції з Django і Python
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse  # Функції для рендерингу шаблонів, перенаправлення, отримання об'єктів або створення HTTP-відповідей
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash  # Функції для роботи з автентифікацією та сесіями користувачів
from django.contrib.auth.decorators import login_required  # Декоратор, що обмежує доступ до функцій тільки для авторизованих користувачів
from .models import Quiz, Question, Answer, Result, UserProfile  # Імпортуємо моделі, створені в проєкті
from django.contrib.auth.models import User  # Стандартна модель користувача Django
from random import sample  # Для випадкового вибору елементів
from django.db.models import Count  # Для агрегації даних
from .models import Quiz, Question, Answer
from .forms import QuizForm, QuestionForm, AnswerForm
from django.contrib import messages

# Реєстрація нового користувача
def register(request):
    if request.method == 'POST':  # Перевірка, чи це POST-запит
        username = request.POST['username']  # Отримуємо ім'я користувача
        password = request.POST['password']  # Отримуємо пароль
        date_of_birth = request.POST['date_of_birth']  # Отримуємо дату народження
        if not User.objects.filter(username=username).exists():  # Перевірка, чи користувач вже існує
            user = User.objects.create_user(username=username, password=password)  # Створення користувача
            UserProfile.objects.create(user=user, date_of_birth=date_of_birth)  # Створення профілю користувача
            return redirect('login')  # Перенаправлення на сторінку входу
    return render(request, 'quiz/register.html')  # Повертаємо сторінку реєстрації

# Вхід користувача
def user_login(request):
    if request.method == 'POST':  # Перевірка POST-запиту
        username = request.POST['username']  # Отримуємо ім'я користувача
        password = request.POST['password']  # Отримуємо пароль
        user = authenticate(request, username=username, password=password)  # Аутентифікація користувача
        if user:  # Якщо користувач успішно автентифікований
            login(request, user)  # Авторизація користувача
            return redirect('home')  # Перенаправлення на домашню сторінку
    return render(request, 'quiz/login.html')  # Повертаємо сторінку входу

# Домашня сторінка (доступна тільки авторизованим користувачам)
@login_required
def home(request):
    quizzes = Quiz.objects.all()  # Отримуємо всі доступні квізи
    categories = Quiz.objects.values('category').annotate(count=Count('id')).order_by('category')  # Групуємо квізи за категоріями
    return render(request, 'quiz/home.html', {'quizzes': quizzes, 'categories': categories})  # Рендеримо шаблон домашньої сторінки

# Початок квізу
@login_required
def start_quiz(request, quiz_id=None):
    if quiz_id:  # Якщо переданий ID квізу
        try:
            quiz = Quiz.objects.get(id=quiz_id)  # Отримуємо квіз за ID
            questions = quiz.questions.all()  # Отримуємо всі питання цього квізу
        except Quiz.DoesNotExist:  # Якщо квіз не знайдено
            return HttpResponse("Quiz not found.", status=404)
    else:  # Якщо ID квізу не переданий, створюємо змішаний квіз
        questions = Question.objects.all().distinct().order_by('?')[:20]  # Випадкові 20 питань
        quiz = {'name': 'Mixed Quiz', 'description': 'A quiz with mixed questions from all available quizzes.'}  # Інформація про змішаний квіз

    if not questions.exists():  # Якщо питань немає
        return HttpResponse("No questions available.", status=404)

    quiz = Quiz.objects.get(id=quiz_id)
    if request.method == 'POST':
        score = 0
        for question in quiz.questions.all():
            selected_answer = request.POST.get(str(question.id))
            if selected_answer and Answer.objects.get(id=selected_answer).is_correct:
                score += 1
        Result.objects.create(user=request.user, quiz=quiz, score=score)
        return redirect('results')

    return render(request, 'quiz/quiz.html', {'quiz': quiz, 'questions': questions})  # Рендеримо сторінку квізу

# Перегляд результатів користувача
@login_required
def results(request):
    results = Result.objects.filter(user=request.user)  # Отримуємо результати авторизованого користувача
    return render(request, 'quiz/results.html', {'results': results})  # Рендеримо сторінку результатів

# Вихід користувача
def user_logout(request):
    logout(request)  # Вихід із сесії
    return redirect('login')  # Перенаправлення на сторінку входу

# Перегляд особистих результатів
@login_required
def user_results(request):
    user_results = Result.objects.filter(user=request.user)  # Отримуємо результати авторизованого користувача
    return render(request, 'quiz/user_results.html', {'user_results': user_results})  # Рендеримо сторінку особистих результатів

# Топ-20 результатів для конкретного квізу
def top20(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)  # Отримуємо квіз або повертаємо 404
    top_results = Result.objects.filter(quiz=quiz).order_by('-score')[:20]  # Отримуємо топ-20 результатів за кількістю балів
    return render(request, 'quiz/top20.html', {'quiz': quiz, 'top_results': top_results})  # Рендеримо сторінку топ-20

# Налаштування користувача
@login_required
def settings(request):
    if request.method == 'POST':
        new_password = request.POST.get('password')
        new_dob = request.POST.get('date_of_birth')

        if new_password:
            request.user.set_password(new_password)
            update_session_auth_hash(request, request.user)
            messages.success(request, "Password updated successfully.")

        if new_dob:
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            user_profile.date_of_birth = new_dob
            user_profile.save()
            messages.success(request, "Date of birth updated successfully.")

        return redirect('home')

    return render(request, 'quiz/settings.html')

# Початок змішаного квізу
@login_required
def start_mixed_quiz(request):
    questions = Question.objects.all().distinct().order_by('?')[:20]  # Випадкові 20 питань
    if not questions.exists():  # Якщо питань немає
        return HttpResponse("No questions available.", status=404)

    quiz = {'name': 'Mixed Quiz', 'description': 'A quiz with mixed questions from all available quizzes.'}  # Інформація про змішаний квіз
    return render(request, 'quiz/quiz.html', {'quiz': quiz, 'questions': questions})  # Рендеримо сторінку квізу

# Список категорій квізів
def categories_list(request):
    categories = Quiz.objects.values('category').annotate(count=Count('id')).order_by('category')  # Отримуємо категорії з кількістю квізів
    return render(request, 'quiz/categories_list.html', {'categories': categories})  # Рендеримо сторінку категорій

# Перегляд квізів за категорією
def quizzes_by_category(request, category_name):
    quizzes = Quiz.objects.filter(category=category_name).order_by('name')  # Отримуємо всі квізи в обраній категорії
    return render(request, 'quiz/quizzes_by_category.html', {'category_name': category_name, 'quizzes': quizzes})  # Рендеримо сторінку квізів за категорією

# Управління вікторинами
def manage_quizzes(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/manage_quizzes.html', {'quizzes': quizzes})

# Додавання вікторини
def add_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_quizzes')
    else:
        form = QuizForm()
    return render(request, 'quiz/add_quiz.html', {'form': form})

# Редагування вікторини
def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('manage_quizzes')
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'quiz/edit_quiz.html', {'form': form})

# Видалення вікторини
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz.delete()
    return redirect('manage_quizzes')

# Додавання питання
def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    question = None

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            return redirect('add_question', quiz_id=quiz.id)  # Перенаправлення після збереження
    else:
        form = QuestionForm()

    return render(request, 'quiz/add_question.html', {
        'quiz': quiz,
        'form': form,
        'question': question,
    })

# Редагування питання
def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == "POST":
        # Оновлюємо текст питання
        question.text = request.POST.get('text')
        question.save()

        # Перевіряємо, чи є форма для додавання нової відповіді
        if 'answer_text' in request.POST:
            answer_text = request.POST.get('answer_text')
            is_correct = 'is_correct' in request.POST
            new_answer = Answer(question=question, text=answer_text, is_correct=is_correct)
            new_answer.save()

        # Після збереження відповіді або редагування питання повертаємо на ту ж сторінку
        return redirect('edit_question', question_id=question.id)

    return render(request, 'quiz/edit_question.html', {'question': question})


# Видалення питання
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    quiz = question.quiz

    if request.method == 'POST':
        question.delete()
        return redirect('manage_questions', quiz_id=quiz.id)

    return render(request, 'quiz/confirm_delete_question.html', {
        'question': question,
    })

# Додавання відповіді
def add_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == "POST":
        # Додаємо нову відповідь
        answer_text = request.POST.get('text')
        is_correct = 'is_correct' in request.POST
        new_answer = Answer(question=question, text=answer_text, is_correct=is_correct)
        new_answer.save()

        # Після додавання відповіді перенаправляємо на редагування питання
        return redirect('edit_question', question_id=question.id)

    return render(request, 'quiz/edit_question.html', {'question': question})

# Редагування відповіді
def edit_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    question = answer.question  # Отримуємо питання, до якого належить ця відповідь

    if request.method == "POST":
        answer.text = request.POST.get('text')
        answer.is_correct = 'is_correct' in request.POST
        answer.save()
        return redirect('manage_questions', quiz_id=question.quiz.id)

    return render(request, 'quiz/edit_answer.html', {'answer': answer, 'question': question})

# Видалення відповіді
def delete_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    answer.delete()
    return redirect('manage_quizzes')

def manage_questions(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = quiz.questions.all()

    return render(request, 'quiz/manage_questions.html', {
        'quiz': quiz,
        'questions': questions,
    })