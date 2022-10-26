from .views import *
from django.urls import path


urlpatterns = [
    path('registration/', UserRegistrationAPIView.as_view(), name='user_registration'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),

]
