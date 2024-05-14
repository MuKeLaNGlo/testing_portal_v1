from rest_framework import serializers

from testing import models


class Answer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ('text', 'is_correct')


class Question(serializers.ModelSerializer):
    answers = Answer(many=True, source='answer')

    class Meta:
        model = models.Question
        fields = ('id', 'text', 'answers')


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

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        test = models.Test.objects.create(**validated_data)
        for question_data in questions_data:
            answers_data = question_data.pop('answers', [])
            question = models.Question.objects.create(**question_data)
            test.questions.add(question)
            for answer_data in answers_data:
                models.Answer.objects.create(question=question, **answer_data)
        return test

    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions', [])

        instance = super().update(instance, validated_data)

        if questions_data:
            for question_data in questions_data:
                answers_data = question_data.pop('answers', [])
                question_id = question_data.pop('id', None)
                if question_id:
                    question = models.Question.objects.get(id=question_id)
                    for key, value in question_data.items():
                        setattr(question, key, value)
                    question.save()
                else:
                    question = models.Question.objects.create(**question_data)
                instance.questions.add(question)

                for answer_data in answers_data:
                    answer_id = answer_data.pop('id', None)
                    if answer_id:
                        answer = models.Answer.objects.get(id=answer_id)
                    for key, value in answer_data.items():
                        setattr(answer, key, value)
                    answer.save()
                else:
                    models.Answer.objects.create(question=question, **answer_data)
        return instance
