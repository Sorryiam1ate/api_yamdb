import django_filters
from django_filters import rest_framework as filters

from reviews.models import Title


class TitleFilter(filters.FilterSet):
    genre = filters.CharFilter(field_name="genre__slug", lookup_expr="iexact")
    category = django_filters.CharFilter(
        field_name='category__slug', lookup_expr='exact')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ("genre", "category", "year", "name")
