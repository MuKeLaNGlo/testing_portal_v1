from rest_framework.viewsets import ModelViewSet

from testing import filters, models, serializers


class Test(ModelViewSet):
    """Тесты"""
    queryset = models.Test.objects.all()
    filter_class = filters.TestFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.TestPreview
        if self.action == 'retrieve':
            return serializers.TestRead
        if self.action == 'create':
            return serializers.TestCreate
