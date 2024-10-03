from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    CategorySerializer,
    GenreSerializer,
    UsersSerializer,
    NoAdminSerializer,
    SignupSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer
)

from reviews.models import Category, Genre, Titles, User, Review
from .permissions import (
    IsAdminOrReadOnly,
    IsOwnerOrModeratorAdmin,
    ModeratorAdmin,
    AdminOnly,
)


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

    serializer_class = ReviewSerializer
    permission_classes = [
        IsOwnerOrModeratorAdmin,
    ]


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    filterset_fields = ('category', 'genre', 'name', 'year')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleWriteSerializer
