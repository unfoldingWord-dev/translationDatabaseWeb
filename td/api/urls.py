from django.conf.urls import url

from .views import questionnaire_json, templanguages_json, lang_assignment_json, lang_assignment_changed_json


urlpatterns = [
    url(r"^questionnaire/$", questionnaire_json, name="questionnaire"),
    url(r"^templanguages/$", templanguages_json, name="templanguages"),
    url(r"^templanguages/assignment/$", lang_assignment_json, name="templanguages_assignment"),
    url(r"^templanguages/assignment/changed/$", lang_assignment_changed_json, name="templanguages_changed"),
]
