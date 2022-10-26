from django.urls import path, include
from django.views.decorators.http import require_http_methods
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'course', CourseViewSet)
router.register(r'category', CategoryViewsSet)
router.register(r'unit', UnitViewSet)
router.register('attended-course', AttendedCourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:course_pk>/reviews/', require_http_methods(['GET', 'POST'])(ReviewViewSet.as_view({'get': 'list', 'post': 'create'}))),
    path('<int:course_pk>/reviews/<int:review_pk>/', require_http_methods(['DELETE'])(ReviewViewSet.as_view({'delete': 'destroy'})))
]
