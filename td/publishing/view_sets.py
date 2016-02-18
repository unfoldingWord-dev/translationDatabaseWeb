from django.db.models import Count, Max
from django.http import Http404, JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.response import Response
from td.publishing.models import PublishRequest, ResourceDocument
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


class OfficialResourcesViewSet(viewsets.ViewSet):
    """
    Gets the list of approved/published resource types
    """

    @staticmethod
    def list(request, **kwargs):

        if 'version' in kwargs:
            return OfficialResourcesViewSet.get_json(kwargs['res_type'], kwargs['lang_code'], kwargs['version'])
            pass

        if 'lang_code' in kwargs:
            return OfficialResourcesViewSet.get_resource_versions(request, kwargs['res_type'], kwargs['lang_code'])

        if 'res_type' in kwargs:
            return OfficialResourcesViewSet.get_resource_languages(request, kwargs['res_type'])

        return OfficialResourcesViewSet.get_resource_types(request)

    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return AllowAny(),

        return DenyAll(),

    @staticmethod
    def get_resource_types(request):
        """
        Gets a list of approved/published resource types.
        :param Request request:
        :return: Response
        """
        queryset = ResourceDocument.objects.values('resource_type__short_name').annotate(Count('id')).order_by(
            'resource_type__short_name')
        return_val = []
        for obj in queryset:
            return_val.append(
                {obj['resource_type__short_name']: request.build_absolute_uri(obj['resource_type__short_name'])})
        return Response(return_val)

    @staticmethod
    def get_resource_languages(request, resource_type):
        """
        Gets a list of the languages that have a specific resource published.
        :param Request request:
        :param str|unicode resource_type:
        :return: Response
        """
        queryset = ResourceDocument.objects.filter(resource_type__short_name=resource_type).values(
            'language__code').annotate(Count('id')).order_by('language__code')
        return_val = []
        for obj in queryset:
            return_val.append({obj['language__code']: request.build_absolute_uri(obj['language__code'])})
        return Response(return_val)

    # noinspection PyUnusedLocal
    @staticmethod
    def get_resource_versions(request, resource_type, language_code):
        """
        Get the available versions of this resource
        :param Request request:
        :param str|unicode resource_type:
        :param str|unicode language_code:
        :return:
        """
        # there is no way to specify a version yet, so 'latest' is the only value
        return_val = [{'latest': request.build_absolute_uri('latest')}]
        return Response(return_val)

    @staticmethod
    def get_json(resource_type, language_code, version):

        if version == 'latest':
            result = ResourceDocument.objects.filter(resource_type__short_name=resource_type,
                                                     language__code=language_code).values(
                'language__code').annotate(Max('id'))

            # return 404 if not found
            if not result or result.count() < 1:
                raise Http404

            id_max = result[0]['id__max']

            result = ResourceDocument.objects.filter(id=id_max).values('json_data').first()

            return JsonResponse(result['json_data'])
