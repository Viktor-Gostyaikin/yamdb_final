from rest_framework import viewsets
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)


class ListOrCreateOrDestroy(ListModelMixin, CreateModelMixin,
                            DestroyModelMixin, viewsets.GenericViewSet):
    pass
