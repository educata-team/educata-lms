from django.urls import path

from .views import *


urlpatterns = [
    path('', FormInputQuestionViewSet.as_view({'get': 'list', 'post': 'create'})),
]
