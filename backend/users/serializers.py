from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.state import token_backend

from .models import *


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = User
        exclude = ['created_at', 'updated_at', 'last_login', 'is_admin', 'is_active', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data.get('username'),
                                        email=validated_data.get('email'),
                                        password=validated_data.get('password'),
                                        avatar=validated_data.get('avatar'),
                                        bio=validated_data.get('bio'),
                                        last_name=validated_data.get('last_name'),
                                        first_name=validated_data.get('first_name'))
        return {
                'id': user.pk,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
                }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'is_active', 'created_at', 'is_admin', 'updated_at', 'last_login']


class MyTokenObtainSerizalier(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        # Add extra responses here
        data['user_id'] = self.user.pk
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['role'] = user.role
        return token


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super(CustomTokenRefreshSerializer, self).validate(attrs)
        decoded_payload = token_backend.decode(data['access'], verify=True)
        user_uid = decoded_payload['user_id']
        # add filter query
        data.update({'user_id': user_uid})
        return data
