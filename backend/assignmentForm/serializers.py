from rest_framework.serializers import ModelSerializer, IntegerField, CharField

from assignmentForm.models import *
from drf_extra_fields.fields import Base64FileField


class FormInputQuestionSerializer(ModelSerializer):

    class Meta:
        model = FormInputQuestion
        fields = '__all__'


class FormChoiceQuestionSerializer(ModelSerializer):

    class Meta:
        model = FormChoiceQuestion
        fields = '__all__'


class FormFileQuestionSerializer(ModelSerializer):

    class Meta:
        model = FormFileQuestion
        fields = '__all__'
