from rest_framework import serializers

from testing import models


class Answer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = '__all__'


class Question(serializers.ModelSerializer):
    answer = Answer(many=True, source='answers')

    class Meta:
        model = models.Question
        fields = ('id', 'text', 'answer')


class TestRead(serializers.ModelSerializer):
    questions = Question(many=True)

    class Meta:
        model = models.Test
        fields = (
            'title',
            'description',
            'questions',
            'status',
            'duration_minutes',
        )


class TestPreview(serializers.ModelSerializer):
    class Meta:
        model = models.Test
        fields = ('title', 'status', 'image', 'duration_minutes')


class TestWrite(serializers.ModelSerializer):
    class Meta:
        model = models.Test
        fields = '__all__'


class TestCreate(serializers.ModelSerializer):
    class Meta:
        model = models.Test
        fields = '__all__'
