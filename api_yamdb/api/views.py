from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    CategorySerializer,
    GenreSerializer,
    UsersSerializer,
    NoAdminSerializer,
    SignupSerializer,
    ReviewSerializer, TokenSerializer,
)

from reviews.models import Category, Genre, Titles, User, Review
from .permissions import (
    IsAdminOrReadOnly,
    IsOwnerOrModeratorAdmin,
    ModeratorAdmin,
    AdminOnly,
)
from .utils import generate_confirmation_code


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated, AdminOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['GET', 'PATCH', ],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UsersSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = NoAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class APIToken(TokenObtainPairView):
    serializer_class = TokenSerializer

    # def post(self, request):
    #     serializer = TokenSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     data = serializer.validated_data
    #     try:
    #         user = User.objects.get(username=data['username'])
    #     except User.DoesNotExist:
    #         return Response(
    #             {'username': 'User has not been found.'},
    #             status=status.HTTP_404_NOT_FOUND)
    #     if data.get('confirmation_code') == user.confirmation_code:
    #         token = RefreshToken.for_user(user).access_token
    #         return Response({'token': str(token)},
    #                         status=status.HTTP_201_CREATED)
    #     return Response(
    #         {'confirmation_code': 'Invalid confirmation code!'},
    #         status=status.HTTP_400_BAD_REQUEST)


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
        serializer = SignupSerializer(data=request.data)
        if User.objects.filter(username=request.data.get('username'),
                               email=request.data.get('email')).exists():
            self.send_confirmation_code(request)
            return Response(request.data, status=status.HTTP_200_OK)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.send_confirmation_code(request)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
