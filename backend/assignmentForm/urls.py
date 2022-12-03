from django.urls import path

from .views import *


urlpatterns = [
    path('input-question/', FormInputQuestionViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('input-question/<int:form_input_question_pk>/', FormInputQuestionViewSet.as_view({'put': 'update', 'delete': 'destroy'}))
]
