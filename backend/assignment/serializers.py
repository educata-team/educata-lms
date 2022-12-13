from rest_framework.fields import IntegerField, CharField
from rest_framework.serializers import ModelSerializer
from drf_extra_fields.fields import Base64FileField

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
    user = IntegerField(source='user.pk', required=False)

    class Meta:
        model = AssignmentChoiceAnswer
        fields = '__all__'


class AssignmentInputAnswerSerializer(ModelSerializer):
    user = IntegerField(source='user.id', required=False)

    class Meta:
        model = AssignmentInputAnswer
        fields = '__all__'


class AssigmentFileAnswerSerializer(ModelSerializer):
    user = IntegerField(source='user.id', required=False)
    file = Base64FileField()

    class Meta:
        model = AssignmentFileAnswer
        fields = '__all__'
