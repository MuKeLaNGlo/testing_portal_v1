from django_filters import rest_framework as django_filters
from django.db.models import Q, QuerySet

from testing import consts, models


class TestFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    order_by = django_filters.OrderingFilter(
        fields=(
            'id',
            'title',
            'description',
            ('usertests__completed', 'completed'),
            'tag',
        )
    )
    tag = django_filters.CharFilter(method='filter_tag')
    term = django_filters.CharFilter(method='filter_term')
    difficulty = django_filters.ChoiceFilter(choices=consts.DIFFICULTY_CHOICES)
    class Meta:
        model = models.Test
        fields = [
            'id',
            'title',
            'description',
            'tag',
            'difficulty',
        ]

    def filter_tag(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        return queryset.filter(tag__name__icontains=value)

    def filter_term(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value) |
            Q(tag__name__icontains=value)
        )
