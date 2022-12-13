from django.db import models

from course.models import Assignment
from users.models import User


class FormInputQuestion(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    question = models.CharField(max_length=200, verbose_name='Питання')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FormChoiceQuestion(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    question = models.CharField(max_length=200, verbose_name='Питання')
    is_multiple_answer = models.BooleanField(default=False, verbose_name='Питання має декілька відповідей')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FormFileQuestion(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    question = models.CharField(max_length=200, verbose_name='Питання')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FormChoiceOption(models.Model):
    question = models.ForeignKey(FormChoiceQuestion, on_delete=models.CASCADE)
    text = models.CharField(max_length=200, verbose_name='Відповідь')
    correct = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
