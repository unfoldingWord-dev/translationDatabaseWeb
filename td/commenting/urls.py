from django.conf.urls import url

from .views import PostCommentView, DeleteCommentView


urlpatterns = [
    url(r"^post/$", PostCommentView.as_view(), name="post_comment"),
    url(r"^delete/(?P<id>\d+)/$", DeleteCommentView.as_view(), name="delete_comment"),
]
