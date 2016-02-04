from django.conf.urls import include, url
from td.publishing.view_sets import PublishRequestViewSet, ApprovedRequestViewSet, RejectedRequestViewSet
from rest_framework import routers


# routers for the REST API
router = routers.DefaultRouter()
router.register(r'publish-requests', PublishRequestViewSet, base_name="publish_requests")
router.register(r'approved-requests', ApprovedRequestViewSet, base_name="approved_requests")
router.register(r'rejected-requests', RejectedRequestViewSet, base_name="rejected_requests")

urlpatterns = [
    url(r'^', include(router.urls)),
]
