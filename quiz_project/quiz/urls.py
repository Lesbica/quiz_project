from django.urls import path  # Імпортуємо функцію `path` для визначення маршрутів (URL-шляхів).
from . import views  # Імпортуємо модуль `views`, де реалізовані функції, що обробляють маршрути.

urlpatterns = [  # Список маршрутів, кожен з яких прив'язаний до певного view.
    path('register/', views.register, name='register'),
    # Маршрут для сторінки реєстрації.
    # 'register/' — шлях у браузері, `views.register` — функція у views.py, яка обробляє цей шлях.
    # name='register' дозволяє використовувати цей маршрут у шаблонах за іменем.

    path('login/', views.user_login, name='login'),
    # Маршрут для сторінки входу в систему. Прив'язаний до функції `user_login`.

    path('logout/', views.user_logout, name='logout'),
    # Маршрут для виходу користувача з системи. Прив'язаний до функції `user_logout`.

    path('', views.home, name='home'),
    # Головна сторінка (порожній шлях). Прив'язана до функції `home`.

    path('quiz/<int:quiz_id>/', views.start_quiz, name='start_quiz'),
    # Динамічний маршрут для старту вікторини за її ID.
    # <int:quiz_id> означає, що очікується ціле число в URL, яке передається у функцію `start_quiz`.

    path('results/', views.results, name='results'),
    # Маршрут для перегляду всіх результатів. Прив'язаний до функції `results`.

    path('user_results/', views.user_results, name='user_results'),
    # Маршрут для перегляду результатів поточного користувача. Прив'язаний до функції `user_results`.

    path('quiz/<int:quiz_id>/top20/', views.top20, name='top20'),
    # Динамічний маршрут для перегляду топ-20 результатів для конкретної вікторини.
    # Прив'язаний до функції `top20`.

    path('settings/', views.settings, name='settings'),
    # Маршрут для налаштувань користувача. Прив'язаний до функції `settings`.

    path('mixed-quiz/', views.start_mixed_quiz, name='start_mixed_quiz'),
    # Маршрут для старту змішаної вікторини, яка об'єднує питання з різних категорій.
    # Прив'язаний до функції `start_mixed_quiz`.

    path('categories/', views.categories_list, name='categories_list'),
    # Маршрут для перегляду списку всіх категорій. Прив'язаний до функції `categories_list`.

    path('categories/<str:category_name>/', views.quizzes_by_category, name='quizzes_by_category'),
    # Динамічний маршрут для перегляду вікторин за певною категорією.
    # <str:category_name> означає, що очікується рядок в URL, який передається у функцію `quizzes_by_category`.
    path('manage_quizzes/', views.manage_quizzes, name='manage_quizzes'),
    path('add_quiz/', views.add_quiz, name='add_quiz'),
    path('edit_quiz/<int:quiz_id>/', views.edit_quiz, name='edit_quiz'),
    path('delete_quiz/<int:quiz_id>/', views.delete_quiz, name='delete_quiz'),
    path('add_question/<int:quiz_id>/', views.add_question, name='add_question'),
    path('delete_question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('add_answer/<int:question_id>/', views.add_answer, name='add_answer'),
    path('delete_answer/<int:answer_id>/', views.delete_answer, name='delete_answer'),
path('quiz/<int:quiz_id>/questions/', views.manage_questions, name='manage_questions'),
    path('question/<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('answer/<int:answer_id>/edit/', views.edit_answer, name='edit_answer'),
]
