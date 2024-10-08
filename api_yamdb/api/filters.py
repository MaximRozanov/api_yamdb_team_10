import django_filters
from reviews.models import Title


class TitlesFilter(django_filters.FilterSet):

    category = django_filters.CharFilter(lookup_expr='icontains',
                                         field_name='category__slug')
    genre = django_filters.CharFilter(lookup_expr='icontains',
                                      field_name='genre__slug')
    name = django_filters.CharFilter(lookup_expr='icontains',
                                     field_name='name')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
