from rest_framework import filters
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from .serializers import CategorySerializer, GenreSerializer, ReviewSerializer
from reviews.models import Category, Genre, Titles, Review
from .permissions import IsAdminOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = [
        IsAdminOrReadOnly,
    ]


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = [
        IsAdminOrReadOnly,
    ]


class ReviewViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs['title_id'])
        return Review.objects.filter(title=title)

    serializer_class = ReviewSerializer
