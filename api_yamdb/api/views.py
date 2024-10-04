from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    UsersSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer
)

from reviews.models import Category, Genre, Titles, User, Review, Comment
from .permissions import (
    IsOwnerOrModeratorAdmin,
)
from .filters import TitlesFilter


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class MixinViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CategoryViewSet(MixinViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    # permission_classes = [IsAdminOrReadOnly, ]


class GenreViewSet(MixinViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    # permission_classes = [IsAdminOrReadOnly, ]


class ReviewViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs['title_id'])
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs['title_id'])

        queryset = Review.objects.filter(author=self.request.user, title=title)

        if queryset.exists():
            raise ValidationError('Отзыв уже существует')

        serializer.save(author=self.request.user, title=title)

    def perform_update(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)

    serializer_class = ReviewSerializer
    permission_classes = [
        IsOwnerOrModeratorAdmin,
    ]


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleWriteSerializer


class CommentViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        review = get_object_or_404(
            Review.objects.filter(title__id=self.kwargs['title_id']),
            pk=self.kwargs['review_id'],
        )
        return Comment.objects.filter(review=review)

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review.objects.filter(title__id=self.kwargs['title_id']),
            pk=self.kwargs['review_id'],
        )
        serializer.save(author=self.request.user, review=review)

    def perform_update(self, serializer):
        review = get_object_or_404(
            Review.objects.filter(title__id=self.kwargs['title_id']),
            pk=self.kwargs['review_id'],
        )
        serializer.save(author=self.request.user, review=review)

    serializer_class = CommentSerializer
    permission_classes = [
        IsOwnerOrModeratorAdmin,
    ]
