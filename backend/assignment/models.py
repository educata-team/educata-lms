from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from assignmentForm.models import FormChoiceQuestion, FormChoiceOption, FormFileQuestion, FormInputQuestion
from course.models import Assignment
from users.models import User


class AssignmentAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    feedback = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AssignmentChoiceAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(FormChoiceQuestion, on_delete=models.CASCADE)
    answer = models.ForeignKey(FormChoiceOption, on_delete=models.CASCADE, verbose_name='Правильна відповідь')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AssignmentFileAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(FormFileQuestion, on_delete=models.CASCADE)
    file = models.FileField(upload_to='assignments/files')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AssignmentInputAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(FormInputQuestion, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
