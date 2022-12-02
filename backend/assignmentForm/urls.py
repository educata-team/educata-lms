from django.urls import path

from .views import *


urlpatterns = [
    path('', FormInputQuestionModelViewSet.as_view({'get': 'list', 'post': 'create'})),
]
