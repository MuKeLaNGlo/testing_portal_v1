from django_filters import rest_framework as django_filters
from django.db.models import Q, QuerySet

from testing import models


class TestFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    order_by = django_filters.OrderingFilter(
        fields=(
            'id',
            'title',
            'description',
            ('usertests__completed', 'completed')
        )
    )
    term = django_filters.CharFilter(method='filter_term')
    class Meta:
        model = models.Test
        fields = [
            'id',
            'title',
            'description',
        ]

    def filter_term(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value)
        )
