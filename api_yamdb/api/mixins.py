from rest_framework import filters, mixins, viewsets

from api.permissions import IsAdminOrReadOnly


class GetPostDeleteViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
    permission_classes = (IsAdminOrReadOnly,)
