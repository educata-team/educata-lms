# Generated by Django 4.1.2 on 2022-12-13 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assignmentForm', '0003_remove_formchoiceoption_assignment_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='formchoiceoption',
            old_name='choice_question',
            new_name='question',
        ),
    ]