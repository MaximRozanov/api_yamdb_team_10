from rest_framework.routers import DefaultRouter
from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from api.views import (
    CategoryViewSet,
    GenreViewSet,
    ReviewViewSet,
    UsersViewSet,
    CommentViewSet,
)

from api.views import (CategoryViewSet,
                       GenreViewSet,
                       UsersViewSet, 
                       TitlesViewSet)
from api.constants import VERSION

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
    path(f'api/{VERSION}/', include(router_v1.urls)),
    path(
        'api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'
    ),
]
