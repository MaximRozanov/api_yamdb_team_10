from django.core.mail import send_mail
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from api.mixins import MethodPUTNotAllowedMixin
from api.permissions import AdminOnly
from api.utils import generate_confirmation_code
from custom_user.models import User
from custom_user.serializers import UsersSerializer, NoAdminSerializer, TokenSerializer, SignupSerializer


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
