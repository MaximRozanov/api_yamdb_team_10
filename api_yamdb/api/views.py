from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import MethodNotAllowed
from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework import filters, status
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    UsersSerializer,
    NoAdminSerializer,
    SignupSerializer,
    ReviewSerializer,
    TokenSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
)

from reviews.models import Category, Genre, Title, User, Review, Comment
from .permissions import IsAdminOrReadOnly, ModeratorAdmin, AdminOnly
from .utils import generate_confirmation_code
from .filters import TitlesFilter


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, AdminOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=[
            'GET',
            'PATCH',
        ],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me',
    )
    def get_current_user_info(self, request):
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UsersSerializer(
                    request.user, data=request.data, partial=True
                )
            else:
                serializer = NoAdminSerializer(
                    request.user, data=request.data, partial=True
                )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UsersSerializer(request.user)
        return Response(serializer.data)


class APIToken(TokenObtainPairView):
    serializer_class = TokenSerializer


class APISignup(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def send_confirmation_code(request):
        user = get_object_or_404(
            User,
            username=request.data.get('username'),
        )
        user.confirmation_code = generate_confirmation_code()
        user.save()
        send_mail(
            'данные токена',
            f'Код  {user.confirmation_code}',
            'token@yamdb.ru',
            [request.data.get('email')],
        )

    def post(self, request):
        user = User.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email'),
        )
        if user.exists():
            self.send_confirmation_code(request)
            return Response(request.data, status=status.HTTP_200_OK)
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.send_confirmation_code(request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryGenreMixinViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class MixinViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise MethodNotAllowed('PUT запросы не разрешены.')
        return super().update(request, *args, **kwargs)


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


class ReviewViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])

        queryset = Review.objects.filter(author=self.request.user, title=title)

        if queryset.exists():
            raise ValidationError('Отзыв уже существует')

        serializer.save(author=self.request.user, title=title)

    def perform_update(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)

    serializer_class = ReviewSerializer
    permission_classes = [
        ModeratorAdmin,
    ]


class TitlesViewSet(MixinViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    permission_classes = [
        IsAdminOrReadOnly,
    ]

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
        ModeratorAdmin,
    ]
