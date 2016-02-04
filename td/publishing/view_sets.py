from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.response import Response
from td.publishing.models import PublishRequest
from td.publishing.serializers import PublishRequestSerializer, ApprovedRequestSerializer, RejectedRequestSerializer


class DenyAll(BasePermission):
    """
    Deny access to everyone.
    """
    def has_permission(self, request, view):
        return False


class PublishRequestViewSet(viewsets.ModelViewSet):
    queryset = PublishRequest.objects.filter(approved_at__isnull=True, rejected_at__isnull=True)
    serializer_class = PublishRequestSerializer
    lookup_field = 'pk'
    lookup_value_regex = '[0-9]+'

    def get_permissions(self):
        # allow non-authenticated user to create via POST
        if self.request.method in ['POST', 'GET', 'HEAD', 'OPTIONS']:
            return AllowAny(),

        return DenyAll(),

    # noinspection PyUnusedLocal
    @detail_route()
    def get_publish_request(self, request, pk=None):
        """
        Returns the selected PublishRequest object
        :param rest_framework.request.Request request: Not used
        :param unicode pk: The id of the PublishRequest object to return
        :return: Response
        """
        pk_filter = {'pk': pk}
        obj = get_object_or_404(self.get_queryset(), **pk_filter)
        serializer = self.serializer_class(obj)
        return Response(serializer.data)


class RejectedRequestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PublishRequest.objects.filter(rejected_at__isnull=False)
    serializer_class = RejectedRequestSerializer

    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return AllowAny(),

        return DenyAll(),


class ApprovedRequestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PublishRequest.objects.filter(approved_at__isnull=False, rejected_at__isnull=True)
    serializer_class = ApprovedRequestSerializer

    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return AllowAny(),

        return DenyAll(),
