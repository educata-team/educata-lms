from .views import *
from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('registration/', UserRegistrationAPIView.as_view(), name='user_registration'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('refresh/', MyRefreshToken.as_view(), name='refresh-token'),
    path('user/<int:user_pk>/', UserRetrieveAPIView.as_view(), name='user-detail'),
]
