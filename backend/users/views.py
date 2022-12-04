from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import *


class UserRegistrationAPIView(CreateAPIView):
    model = User
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            response = serializer.save()
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveAPIView(RetrieveAPIView):
    model = User
    serializer_class = UserSerializer

    def get_object(self):
        try:
            return User.objects.get(pk=self.kwargs.get('user_pk'))
        except ObjectDoesNotExist:
            return None

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            serializer = self.get_serializer(instance=instance)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data={'detail': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainSerizalier


class MyRefreshToken(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer
