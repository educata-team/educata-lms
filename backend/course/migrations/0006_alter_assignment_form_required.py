# Generated by Django 4.1.2 on 2022-12-05 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_remove_assignment_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='form_required',
            field=models.BooleanField(default=True, verbose_name='Завдання, яке вимагає відповідь письмову або тестову'),
        ),
    ]
