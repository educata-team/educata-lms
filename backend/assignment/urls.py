from django.urls import path

from .views import *


urlpatterns = [
    path('answer/', AssignmentAnswerViewSet.as_view({'post': 'create'}), name='answers')
    # path('input-answer/', AssignmentInputAnswerViewSet.as_view({'post': 'create'}), name='assignment-input-answers'),
    # path('choice-answer/', AssignmentChoiceAnswerViewSet.as_view({'post': 'create'}, name='assignment-choice-answers')),
]
