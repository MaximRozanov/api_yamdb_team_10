from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Avg, IntegerField

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
from .mixins import CategoryGenreMixinViewSet, MethodPUTNotAllowedMixin


class UsersViewSet(MethodPUTNotAllowedMixin):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, AdminOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

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
        queryset = Review.objects.filter(
            author=self.request.user, title=self.get_title()
        )

        if queryset.exists():
            raise ValidationError('Отзыв уже существует')

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
