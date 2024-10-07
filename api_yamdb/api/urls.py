from rest_framework.routers import DefaultRouter
from django.urls import include, path

from api.views import (
    CategoryViewSet,
    GenreViewSet,
    ReviewViewSet,
    CommentViewSet,
)

from api.views import (
    CategoryViewSet,
    GenreViewSet,
    TitlesViewSet,
)

from api.views import CategoryViewSet, GenreViewSet
from custom_user.views import APIToken, APISignup, UsersViewSet

router_v1 = DefaultRouter()

router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register('genres', GenreViewSet, basename='genre')
router_v1.register('users', UsersViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews',
)
router_v1.register('titles', TitlesViewSet, basename='title')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('api/v1/auth/token/', APIToken.as_view(), name='token'),
    path('api/v1/', include(router_v1.urls)),
    path('api/v1/auth/signup/', APISignup.as_view(), name='signup'),
]
