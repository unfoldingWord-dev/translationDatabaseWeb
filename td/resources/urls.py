from django.conf.urls import url

from .views import (
    PublisherListView,
    PublisherDetailView,
    PublisherEditView,
    PublisherCreateView,
    TitleListView,
    TitleDetailView,
    TitleEditView,
    TitleCreateView,
    TempLanguageQuestionnaireView,
)

urlpatterns = [
    url(r"publishers/$", PublisherListView.as_view(), name="publisher_list"),
    url(r"publishers/create/$", PublisherCreateView.as_view(), name="publisher_create"),
    url(r"publishers/(?P<pk>\d+)/$", PublisherDetailView.as_view(), name="publisher_detail"),
    url(r"publishers/(?P<pk>\d+)/edit/$", PublisherEditView.as_view(), name="publisher_edit"),
    url(r"titles/$", TitleListView.as_view(), name="title_list"),
    url(r"titles/create/$", TitleCreateView.as_view(), name="title_create"),
    url(r"titles/(?P<slug>[-\w\d]+)/$", TitleDetailView.as_view(), name="title_detail"),
    url(r"titles/(?P<slug>[-\w\d]+)/edit/$", TitleEditView.as_view(), name="title_edit"),

    url(r"^questionnaire/(?P<temp_language>\d+)/$", TempLanguageQuestionnaireView.as_view(), name="templanguage_questionnaire"),
]
