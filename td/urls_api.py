from django.conf.urls import include, url
from td.publishing.view_sets import PublishRequestViewSet, ApprovedRequestViewSet, RejectedRequestViewSet, \
    OfficialResourcesViewSet
from rest_framework import routers

# routers for the REST API
router = routers.DefaultRouter()
router.register(r'publish-requests', PublishRequestViewSet, base_name="publish_requests")
router.register(r'approved-requests', ApprovedRequestViewSet, base_name="approved_requests")
router.register(r'rejected-requests', RejectedRequestViewSet, base_name="rejected_requests")
router.register(r"official-resources", OfficialResourcesViewSet, base_name="official_resources")
router.register(r"official-resources/(?P<res_type>[-_\w]+)", OfficialResourcesViewSet, base_name="official_resources")
router.register(r"official-resources/(?P<res_type>[-_\w]+)/(?P<lang_code>[-_\w]+)", OfficialResourcesViewSet,
                base_name="official_resources")
router.register(r"official-resources/(?P<res_type>[-_\w]+)/(?P<lang_code>[-_\w]+)/(?P<version>[-_\w]+)",
                OfficialResourcesViewSet, base_name="official_resources")

urlpatterns = [
    url(r'^', include(router.urls)),
]
