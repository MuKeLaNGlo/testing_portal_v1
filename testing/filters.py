from django_filters import rest_framework as django_filters

from testing import models


class TestFilter(django_filters.FilterSet):
    class Meta:
        model = models.Test
        fields = [
            'id',
            'title',
            'description',
        ]
