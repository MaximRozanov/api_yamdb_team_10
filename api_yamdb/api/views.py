from rest_framework import filters
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from .serializers import (CategorySerializer,
                          GenreSerializer,
                          UsersSerializer,
                          NoAdminSerializer,
                          SignupSerializer)

from reviews.models import Category, Genre, Titles, User
from .permissions import IsAdminOrReadOnly, ModeratorAdmin, AdminOnly


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
    viewsets.GenericViewSet
):
    pass


class CategoryViewSet(MixinViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'
    # permission_classes = [IsAdminOrReadOnly, ]


class GenreViewSet(MixinViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'
    # permission_classes = [IsAdminOrReadOnly, ]
