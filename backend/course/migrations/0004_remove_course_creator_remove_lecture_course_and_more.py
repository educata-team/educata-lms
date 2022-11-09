# Generated by Django 4.1.2 on 2022-11-01 22:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0003_alter_course_editors_alter_course_evaluators_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='lecture',
            name='course',
        ),
        migrations.AddField(
            model_name='unit',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.course'),
        ),
        migrations.AlterField(
            model_name='course',
            name='editors',
            field=models.ManyToManyField(related_name='editors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='course',
            name='evaluators',
            field=models.ManyToManyField(related_name='evaluators', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='course',
            name='managers',
            field=models.ManyToManyField(related_name='managers', to=settings.AUTH_USER_MODEL),
        ),
    ]
