from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name='Назва')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name='Назва')
    description = models.TextField(verbose_name='Опис')
    logo = models.ImageField(upload_to='courses/logos', verbose_name='Лого')
    banner = models.ImageField(upload_to='courses/banners', verbose_name='Банер')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    evaluators = models.ManyToManyField(User, related_name='evaluators')
    editors = models.ManyToManyField(User, related_name='editors')
    managers = models.ManyToManyField(User, related_name='managers')


class Unit(models.Model):
    title = models.CharField(max_length=200, verbose_name='Назва')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Lecture(models.Model):
    title = models.CharField(max_length=200, verbose_name='Назва')
    body = models.TextField(verbose_name='Вміст курсу')
    video_url = models.URLField(blank=True, null=True, verbose_name='Посилання на відео')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AttendedCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_message = models.CharField(max_length=200, verbose_name='Огляд')
    rating = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)], verbose_name='Оцінка')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Assignment(models.Model):
    title = models.CharField(max_length=200, verbose_name='Назва')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name='Юніт')
    description = models.TextField(verbose_name='Опис')
    file_required = models.BooleanField(verbose_name='Завдання, яке вимагає файлову відопвідь', default=False)
    form_required = models.BooleanField(verbose_name='Завдання, яке вимагає відповідь письмову або тестову', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
