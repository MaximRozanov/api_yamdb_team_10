from rest_framework.routers import SimpleRouter
from django.urls import include, path


from api.views import (
    CategoryViewSet,
    GenreViewSet,
    ReviewViewSet,
    UsersViewSet,
)

router_v1 = SimpleRouter()
router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register('genres', GenreViewSet, basename='genre')
router_v1.register('users', UsersViewSet, basename='users')
router_v1.register(
    r'titles/(?P<titles_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews',
)

urlpatterns = [
    path('', include(router_v1.urls)),
]
