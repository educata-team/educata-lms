from rest_framework.serializers import ModelSerializer

from assignmentForm.models import *


class FormInputQuestionSerializer(ModelSerializer):

    class Meta:
        model = FormInputQuestion
        fields = '__all__'


class FormChoiceQuestionSerializer(ModelSerializer):

    class Meta:
        model = FormChoiceQuestion
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['choices'] = FormChoiceOptionSerializer(FormChoiceOption.objects
                                                     .select_related('question').filter(question__pk=instance.pk),
                                                     many=True).data
        return data


class FormFileQuestionSerializer(ModelSerializer):

    class Meta:
        model = FormFileQuestion
        fields = '__all__'


class FormChoiceOptionSerializer(ModelSerializer):

    class Meta:
        model = FormChoiceOption
        fields = '__all__'
