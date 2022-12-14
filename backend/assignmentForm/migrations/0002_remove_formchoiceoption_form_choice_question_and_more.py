# Generated by Django 4.1.2 on 2022-11-30 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_remove_assignment_course'),
        ('assignmentForm', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formchoiceoption',
            name='form_choice_question',
        ),
        migrations.RemoveField(
            model_name='formchoicequestion',
            name='form_model',
        ),
        migrations.RemoveField(
            model_name='formfilequestion',
            name='form_model',
        ),
        migrations.RemoveField(
            model_name='forminputquestion',
            name='form_model',
        ),
        migrations.AddField(
            model_name='formchoiceoption',
            name='assignment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='course.assignment'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='formchoicequestion',
            name='assignment',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='course.assignment'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='formfilequestion',
            name='assignment',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='course.assignment'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='forminputquestion',
            name='assignment',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to='course.assignment'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='FormModel',
        ),
    ]
