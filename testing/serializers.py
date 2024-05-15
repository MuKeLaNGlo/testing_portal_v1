from rest_framework import serializers

from testing import models


class Answer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ('text', 'is_correct')


class Question(serializers.ModelSerializer):
    answers = Answer(many=True)

    class Meta:
        model = models.Question
        fields = ('id', 'text', 'answers')


class TestRead(serializers.ModelSerializer):
    questions = Question(many=True)
    progress_persent = serializers.SerializerMethodField()

    class Meta:
        model = models.Test
        fields = (
            'title',
            'description',
            'questions',
            'status',
            'duration_minutes',
            'progress_persent',
        )

    def get_progress_persent(self, obj):
        user = self.context['request'].user
        try:
            user_test = obj.usertests.get(user=user)
            if user_test.completed:
                total_questions = user_test.test.questions.count()
                correct_answers = user_test.usertestresults.filter(is_correct=True).count()
                if total_questions > 0:
                    return (correct_answers / total_questions) * 100
                return 0
            return 0
        except models.UserTest.DoesNotExist:
            return 0


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

class AnswerSubmitSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    selected_answer_id = serializers.IntegerField()

    def validate(self, data):
        try:
            question = Question.objects.get(id=data['question_id'])
        except Question.DoesNotExist:
            raise serializers.ValidationError(f'Вопрос с id {data["question_id"]} не существует.')

        try:
            selected_answer = Answer.objects.get(id=data['selected_answer_id'])
        except Answer.DoesNotExist:
            raise serializers.ValidationError(f'Ответ с id {data["selected_answer_id"]} не  существует.')

        if selected_answer.question.id != question.id:
            raise serializers.ValidationError('Выбранный ответ не связан с данным вопросом.')
        return data

class TestSubmitSerializer(serializers.Serializer):
    answers = serializers.ListField(child=AnswerSubmitSerializer())
