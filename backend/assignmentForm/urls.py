from django.urls import path

from .views import *


urlpatterns = [
    path('question/', FormQuestionsViewSet.as_view({'post': 'create', 'put': 'update'})),
    path('input-question/', FormInputQuestionViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('input-question/<int:form_input_question_pk>/', FormInputQuestionViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('choice-question/', FormChoiceQuestionViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('choice-question/<int:choice_question_pk>/', FormChoiceQuestionViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('file-question/', FormFileQuestionViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('file-question/<int:file_question_pk>/', FormFileQuestionViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('choice-question/choice/', FormChoiceOptionViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'})),
]
