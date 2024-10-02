from rest_framework.routers import DefaultRouter
from django.urls import include, path

from api.views import CategoryViewSet, GenreViewSet, UsersViewSet
from api.constants import VERSION

router_v1 = DefaultRouter()
router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register('genres', GenreViewSet, basename='genre')
router_v1.register('users', UsersViewSet, basename='users')

urlpatterns = [path(f'api/{VERSION}/', include(router_v1.urls)), ]
