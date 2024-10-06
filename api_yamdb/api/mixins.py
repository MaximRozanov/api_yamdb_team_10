from rest_framework.exceptions import MethodNotAllowed
from rest_framework import viewsets, mixins


class CategoryGenreMixinViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class MethodPUTNotAllowedMixin(viewsets.ModelViewSet):

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise MethodNotAllowed('PUT запросы не разрешены.')
        return super().update(request, *args, **kwargs)
