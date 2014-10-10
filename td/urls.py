from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin


urlpatterns = patterns(
    "",
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),

    url(r"^exports/codes-d43.txt$", "td.views.codes_text_export", name="codes_text_export"),
    url(r"^exports/langnames.txt$", "td.views.names_text_export", name="names_text_export"),
    url(r"^exports/langnames.json$", "td.views.names_json_export", name="names_json_export"),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
