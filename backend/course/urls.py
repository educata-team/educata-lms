from django.urls import path, include
from django.views.decorators.http import require_http_methods

from .routers import *


urlpatterns = [
    path('', include(router.urls)),
    path('<int:course_pk>/unit/', UnitListCreateAPIView.as_view(), name='unit-list-create'),
    path('<int:course_pk>/unit/<int:unit_pk>/', UnitRetrieveUpdateDestroyAPIView.as_view(), name='unit-get-update-delete'),
    path('<int:course_pk>/reviews/', require_http_methods(['GET', 'POST'])(ReviewViewSet.as_view({'get': 'list', 'post': 'create'}))),
    path('<int:course_pk>/reviews/<int:review_pk>/', require_http_methods(['DELETE'])(ReviewViewSet.as_view({'delete': 'destroy'}))),
    path('<int:course_pk>/<int:unit_pk>/assignments/', AssignmentListCreateAPIView.as_view()),
]
