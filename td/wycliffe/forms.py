from django import forms

from .models import (
    Country,
    Language,
    Resource,
    Scripture,
    TranslationNeed,
    WorkInProgress
)


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = [
            "population",
            "primary_networks"
        ]


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = [
            "living_language",
            "gateway_dialect",
            "native_speakers",
            "networks_translating"
        ]


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = [
            "name",
            "copyright",
            "copyright_holder",
            "license"
        ]


class ScriptureForm(forms.ModelForm):
    class Meta:
        model = Scripture
        fields = [
            "kind",
            "bible_content",
            "wip",
            "year",
            "publisher"
        ]


class TranslationNeedForm(forms.ModelForm):
    class Meta:
        model = TranslationNeed
        fields = [
            "text_gaps",
            "text_updates",
            "other_gaps",
            "other_updates"
        ]


class WorkInProgressForm(forms.ModelForm):
    class Meta:
        model = WorkInProgress
        fields = [
            "kind",
            "bible_content",
            "paradigm",
            "translators",
            "anticipated_completion_date"
        ]
