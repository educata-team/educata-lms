from rest_framework.fields import IntegerField, CharField
from rest_framework.serializers import ModelSerializer
from drf_extra_fields.fields import Base64FileField

from .models import *


class AssignmentAnswerSerializer(ModelSerializer):
    user = IntegerField(source='user.id', required=False)
    grade = IntegerField(required=False)
    feedback = CharField(max_length=200, required=False)

    class Meta:
        model = AssignmentAnswer
        fields = '__all__'

    def create(self, validated_data):
        obj = AssignmentAnswer.objects.create(
            user=self.context.get('user'),
            assignment=validated_data.get('assignment')
        )
        return obj

    def update(self, instance, validated_data):
        instance.grade = validated_data.get('grade', None)
        instance.feedback = validated_data.get('feedback', None)
        instance.save()
        return instance

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = instance.user.id
        response['grade'] = instance.grade
        response['feedback'] = instance.feedback
        return response


class AssignmentChoiceAnswerSerializer(ModelSerializer):
    user = IntegerField(source='user.pk', required=False)

    class Meta:
        model = AssignmentChoiceAnswer
        fields = '__all__'

    def create(self, validated_data):
        obj = AssignmentChoiceAnswer.objects.create(
            user=User.objects.get(pk=(validated_data.get('user')).get('pk')),
            question=validated_data.get('question'),
            answer=validated_data.get('answer')
        )
        return obj


class AssignmentInputAnswerSerializer(ModelSerializer):
    user = IntegerField(source='user.id', required=False)

    class Meta:
        model = AssignmentInputAnswer
        fields = '__all__'

    def create(self, validated_data):
        obj = AssignmentInputAnswer.objects.create(
            user=User.objects.get(pk=validated_data.get('user').get('id')),
            question=validated_data.get('question'),
            answer=validated_data.get('answer')
        )
        return obj


class AssigmentFileAnswerSerializer(ModelSerializer):
    user = IntegerField(source='user.id', required=False)
    file = Base64FileField()

    class Meta:
        model = AssignmentFileAnswer
        fields = '__all__'
