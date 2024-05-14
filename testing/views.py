from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from testing import filters, models, serializers, permissions


class Test(ModelViewSet):
    """Тесты"""
    queryset = models.Test.objects.all()
    filter_class = filters.TestFilter
    permission_classes = (permissions.IsInterwierOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.TestPreview
        if self.action == 'retrieve':
            return serializers.TestRead
        if self.action == 'create':
            return serializers.TestWrite

    @action(detail=True, methods=['get'])
    def submit(self, request: Request, *args, **kwargs):
        """Результаты теста"""
        test = self.get_object()
        return Response(test)


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
