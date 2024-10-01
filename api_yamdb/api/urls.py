from rest_framework.routers import SimpleRouter
from django.urls import include, path

from api.views import CategoryViewSet, GenreViewSet

router_v1 = SimpleRouter() 
router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register('genres', GenreViewSet, basename='genre')

urlpatterns = [path('', include(router_v1.urls)), ]