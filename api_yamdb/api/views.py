from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters
from django.db.models import Avg, IntegerField

from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
)

from reviews.models import Category, Genre, Title, Review, Comment
from .permissions import IsAdminOrReadOnly, ModeratorAdmin
from .filters import TitlesFilter
from .mixins import CategoryGenreMixinViewSet, MethodPUTNotAllowedMixin


class CategoryViewSet(CategoryGenreMixinViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = [
        IsAdminOrReadOnly,
    ]


class GenreViewSet(CategoryGenreMixinViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = [
        IsAdminOrReadOnly,
    ]


class ReviewViewSet(MethodPUTNotAllowedMixin):
    serializer_class = ReviewSerializer
    permission_classes = [
        ModeratorAdmin,
    ]

    def get_title_id(self):
        return self.kwargs['title_id']

    def get_title(self):
        return get_object_or_404(Title, pk=self.get_title_id())

    def get_queryset(self):
        return Review.objects.filter(title=self.get_title())

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())

    def perform_update(self, serializer):
        serializer.save(title=self.get_title())


class TitlesViewSet(MethodPUTNotAllowedMixin):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score', output_field=IntegerField())
    )

    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    permission_classes = [
        IsAdminOrReadOnly,
    ]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleWriteSerializer


class CommentViewSet(MethodPUTNotAllowedMixin):
    serializer_class = CommentSerializer
    permission_classes = [
        ModeratorAdmin,
    ]

    def get_title_id(self):
        return self.kwargs['title_id']

    def get_review_id(self):
        return self.kwargs['review_id']

    def get_review(self):
        return get_object_or_404(
            Review.objects.filter(title__id=self.get_title_id()),
            pk=self.get_review_id(),
        )

    def get_queryset(self):
        return Comment.objects.filter(review=self.get_review())

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())

    def perform_update(self, serializer):
        serializer.save(review=self.get_review())
