from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import *


class UserRegistrationAPIView(CreateAPIView):
    model = User
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            response = serializer.save()
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainSerizalier


class MyRefreshToken(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer
