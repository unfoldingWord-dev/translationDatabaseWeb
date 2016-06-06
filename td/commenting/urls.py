from django.conf.urls import url

from .views import PostCommentView


urlpatterns = [
    url(r"^post/$", PostCommentView.as_view(), name="post_comment"),
]
