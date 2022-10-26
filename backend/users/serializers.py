from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from .models import *


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = User
        exclude = ['created_at', 'updated_at', 'last_login', 'is_admin', 'is_active', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],
                                        email=validated_data['email'],
                                        password=validated_data['password'],
                                        avatar=validated_data['avatar'],
                                        bio=validated_data['bio'],
                                        last_name=validated_data['last_name'],
                                        first_name=validated_data['first_name'])
        return {'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
                }


class MyTokenObtainSerizalier(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['role'] = user.role
        return token
