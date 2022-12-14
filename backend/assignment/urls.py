from django.urls import path

from .views import *


urlpatterns = [
    path('', AssignmentAnswerCreateUpdateView.as_view({'post': 'create', 'get': 'retrieve', 'put': 'update'})),
    path('answers/', AssignmentAnswerViewSet.as_view({'post': 'create'}))
    # path('input-answer/', AssignmentInputAnswerViewSet.as_view({'post': 'create'}), name='assignment-input-answers'),
    # path('choice-answer/', AssignmentChoiceAnswerViewSet.as_view({'post': 'create'}, name='assignment-choice-answers')),
]
