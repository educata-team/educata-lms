from django.forms import IntegerField, CharField
from rest_framework.serializers import ModelSerializer

from .models import *


class AssignmentAnswerSerializer(ModelSerializer):
    grade = IntegerField(required=False)
    feedback = CharField(max_length=200, required=False)

    class Meta:
        model = AssignmentAnswer
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['grade'] = instance.grade
        response['feedback'] = instance.feedback
        return response


class AssignmentChoiceAnswerSerializer(ModelSerializer):
    user = IntegerField(source='user.id', required=False)

    class Meta:
        model = AssignmentChoiceAnswer
        fields = '__all__'
