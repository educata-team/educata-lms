from django.forms import IntegerField
from rest_framework.serializers import ModelSerializer

from .models import *


class AssignmentAnswerSerializer(ModelSerializer):
    class Meta:
        model = AssignmentAnswer
        fields = '__all__'


class AssignmentChoiceAnswerSerializer(ModelSerializer):
    user = IntegerField(source='user.id', required=False)

    class Meta:
        model = AssignmentChoiceAnswer
        fields = '__all__'
