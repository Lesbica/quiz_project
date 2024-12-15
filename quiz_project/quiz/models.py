from django.contrib.auth.models import User  # Імпортуємо вбудовану модель User для використання в нашій моделі UserProfile.
from django.db import models  # Імпортуємо модулі для створення моделей.

# Модель профілю користувача, що додає додаткові поля до стандартної моделі User.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Зв'язуємо профіль із користувачем через зв'язок "один до одного". При видаленні User видаляється і UserProfile.
    date_of_birth = models.DateField()  # Поле для зберігання дати народження користувача.

    def __str__(self):
        return self.user.username  # Метод повертає ім'я користувача як текстове представлення моделі.

# Модель для створення вікторин.
class Quiz(models.Model):
    name = models.CharField(max_length=200)  # Поле для назви вікторини, обмежене до 200 символів.
    description = models.TextField()  # Поле для опису вікторини.
    category = models.CharField(max_length=50)  # Поле для категорії вікторини, обмежене до 50 символів.

    def __str__(self):
        return self.name  # Метод повертає назву вікторини як текстове представлення моделі.

# Модель для зберігання питань, що належать до вікторини.
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    # Поле для зв'язку з моделлю Quiz через ForeignKey (зв'язок "багато до одного").
    # Якщо вікторину видаляють, усі пов'язані питання також видаляються.
    text = models.CharField(max_length=300)  # Поле для тексту питання, обмежене до 300 символів.

    def __str__(self):
        return self.text  # Метод повертає текст питання як текстове представлення моделі.

# Модель для зберігання відповідей на питання.
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    # Поле для зв'язку з моделлю Question через ForeignKey (зв'язок "багато до одного").
    # Якщо питання видаляють, усі пов'язані відповіді також видаляються.
    text = models.CharField(max_length=255)  # Поле для тексту відповіді, обмежене до 255 символів.
    is_correct = models.BooleanField(default=False)  # Логічне поле, яке визначає, чи є відповідь правильною.

    def __str__(self):
        return self.text  # Метод повертає текст відповіді як текстове представлення моделі.

# Модель для збереження результатів користувачів у вікторинах.
class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Поле для зв'язку з моделлю User через ForeignKey.
    # Якщо користувача видаляють, усі його результати також видаляються.
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    # Поле для зв'язку з моделлю Quiz через ForeignKey.
    # Якщо вікторину видаляють, усі результати також видаляються.
    score = models.IntegerField()  # Поле для зберігання кількості балів, набраних користувачем.
    date = models.DateTimeField(auto_now_add=True)  # Поле для автоматичного збереження дати створення результату.

    def __str__(self):
        return f"{self.user.username} - {self.quiz.name}"
        # Метод повертає текстове представлення результату у форматі "ім'я користувача - назва вікторини".
