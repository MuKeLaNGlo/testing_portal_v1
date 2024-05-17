from django.contrib.auth.hashers import make_password
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


class Tag(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = '__all__'


class TestRead(serializers.ModelSerializer):
    questions = Question(many=True)
    progress_persent = serializers.SerializerMethodField()
    tag = Tag(many=True)

    class Meta:
        model = models.Test
        fields = (
            'title',
            'description',
            'questions',
            'status',
            'duration_minutes',
            'progress_persent',
            'tag',
            'difficulty',
        )

    def get_progress_persent(self, obj: models.Test):
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
    tag = Tag(many=True)
    class Meta:
        model = models.Test
        fields = ('title', 'status', 'image', 'duration_minutes', 'tag', 'difficulty')


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

    def create(self, validated_data: dict) -> models.Test:
        questions_data = validated_data.pop('questions', [])
        tags_data = validated_data.pop('tag', [])
        test = models.Test.objects.create(**validated_data)
        for question_data in questions_data:
            answers_data = question_data.pop('answers', [])
            question = models.Question.objects.create(**question_data)
            test.questions.add(question)
            for answer_data in answers_data:
                models.Answer.objects.create(question=question, **answer_data)

        for tag_data in tags_data:
            tag = models.Tag.objects.create(**tag_data)
            test.tag.add(tag)
        return test

    def update(self, instance, validated_data: dict) -> models.Test:
        questions_data = validated_data.pop('questions', [])
        tags_data = validated_data.pop('tag', [])
        instance = super().update(instance, validated_data)

        for question_data in questions_data:
            question = models.Question.objects.get(id=question_data['id'])
            instance.questions.add(question)

        instance.tags.clear()
        for tag_data in tags_data:
            tag, created = models.Tag.objects.get_or_create(**tag_data)
            instance.tags.add(tag)
        return instance


class AnswerSubmitSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    selected_answer_id = serializers.IntegerField()

    def validate(self, data: dict) -> dict:
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


class User(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = models.User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'patronymic',
            'username',
            'password',
        )

    def create(self, validated_data: dict) -> models.User:
        validated_data['password'] = make_password(validated_data['password'])
        user = super().create(validated_data)
        return user

    def update(self, instance: models.User, validated_data: dict) -> models.User:
        if validated_data.get('password'):
            validated_data['password'] = make_password(validated_data.get('password'))
        user = super().update(instance, validated_data)
        return user


class AuthorizeRequest(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class AuthorizeResponse(serializers.Serializer):
    is_valid = serializers.BooleanField()
    msg = serializers.CharField(required=False)
    token = serializers.CharField(required=False)
    user = User(required=False)
