import django_filters
from reviews.models import Titles


class TitlesFilter(django_filters.FilterSet):

    category = django_filters.CharFilter(lookup_expr='icontains',
                                         field_name='category__slug')
    genre = django_filters.CharFilter(lookup_expr='icontains',
                                      field_name='genre__slug')
    name = django_filters.CharFilter(lookup_expr='icontains',
                                     field_name='name')
    year = django_filters.NumberFilter(lookup_expr='exact',
                                       field_name='year')

    class Meta:
        model = Titles
        fields = ('category', 'genre', 'name', 'year')
