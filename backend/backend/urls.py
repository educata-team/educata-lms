from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from course.views import *
from . import settings
from .yasg import urlpatterns as yasg_doc


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/assignment/', include('assignmentForm.urls')),
    path('api/v1/courses/', include('course.urls')),
    path('api/v1/users/', include('users.urls')),
]

urlpatterns += yasg_doc

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
