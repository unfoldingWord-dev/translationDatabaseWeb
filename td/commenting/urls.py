from django.conf.urls import url

from .views import post_comment


urlpatterns = [
    url(r"^post/$", post_comment, name="post_comment"),
]
