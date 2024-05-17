from typing import Type

from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from testing import datatools, filters, models, serializers, permissions


class Test(ModelViewSet):
    """Тесты"""
    queryset = models.Test.objects.all()
    filterset_class = filters.TestFilter
    permission_classes = (permissions.IsInterwierOrReadOnly,)

    def get_serializer_class(self) -> Type[ModelSerializer]:
        if self.action == 'list':
            return serializers.TestPreview
        if self.action == 'retrieve':
            return serializers.TestRead
        if self.action == 'create':
            return serializers.TestWrite
        return serializers.TestRead

    def get_serializer_context(self) -> dict:
        return {'request': self.request}

    @extend_schema(
        request=serializers.TestSubmitSerializer,
        responses={
            200: OpenApiResponse(
                response=serializers.TestSubmitSerializer,
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={'detail': 'Тест успешно пройден'},
                    ),
                ],
            ),
            400: OpenApiResponse(
                response=serializers.TestSubmitSerializer,
                examples=[
                    OpenApiExample(
                        'Validation Error',
                        value={'detail': 'Тест уже был пройден!'},
                    ),
                ],
            ),
        },
        examples=[
            OpenApiExample(
                'Пример запроса',
                value={
                    'answers': [
                        {'question_id': 1, 'selected_answer_id': 3},
                        {'question_id': 2, 'selected_answer_id': 4},
                    ]
                },
                request_only=True,
                response_only=False,
            )
        ],
    )
    @action(detail=True, methods=['post'], permission_classes=(permissions.IsAuthenticatedOrReadOnly,))
    def submit(self, request: Request, *args, **kwargs) -> Response:
        """Результаты теста"""
        test = self.get_object()
        user = request.user
        serializer = serializers.TestSubmitSerializer(data=request.data)
        if serializer.is_valid():
            answers_data = serializer.validated_data['answers']

            user_test, _ = models.UserTest.objects.get_or_create(
                user=user,
                test=test,
                defaults={'start_time': timezone.now()},
            )
            if user_test.completed:
                return Response({'detail': 'Тест уже завершен'}, status=status.HTTP_400_BAD_REQUEST)

            for answer in answers_data:
                question_id = answer.get('question_id')
                selected_answer_id = answer.get('selected_answer_id')

                question = models.Question.objects.get(id=question_id)
                selected_answer = models.Answer.objects.get(id=selected_answer_id)

                is_correct = selected_answer.is_correct
                models.UserTestResult.objects.update_or_create(
                    user_test=user_test,
                    question=question,
                    selected_answer=selected_answer,
                    is_correct=is_correct,
                )
            user_test.completed = True
            user_test.end_time = timezone.now()
            user_test.save()
            return Response({'detail': 'Тест успешно пройден'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Question(ModelViewSet):
    """Вопросы"""
    queryset = models.Question.objects.all()
    serializer_class = serializers.Question
    permission_classes = (permissions.IsInterwierOrReadOnly,)


class Answer(ModelViewSet):
    """Ответы"""
    queryset = models.Answer.objects.all()
    serializer_class = serializers.Answer
    permission_classes = (permissions.IsInterwierOrReadOnly,)


class Auth(APIView):
    """Аутентификация пользователя"""
    authentication_classes = []
    permission_classes = []

    @extend_schema(request=serializers.AuthorizeRequest, responses=serializers.AuthorizeResponse)
    def post(self, request: Request) -> Response:
        serializer = serializers.AuthorizeRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = datatools.authorize_user(serializer.validated_data)
        except datatools.AuthorizeError as ex:
            response_data = {'is_valid': False, 'msg': str(ex)}
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)

        user_data = serializers.User(instance=user).data
        response_data = {'is_valid': True, 'token': user.auth_token.key, 'user': user_data}
        return Response(data=response_data, status=status.HTTP_200_OK)
