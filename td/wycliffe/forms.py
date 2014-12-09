from django import forms

from .models import (
    Country,
    Language,
    Network,
    Resource,
    Scripture,
    TranslationNeed,
    WorkInProgress
)


class NetworkForm(forms.ModelForm):
    class Meta:
        model = Network
        fields = [
            "name"
        ]


class CountryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CountryForm, self).__init__(*args, **kwargs)
        self.fields["primary_networks"].widget.attrs["class"] = "select2-multiple"

    class Meta:
        model = Country
        fields = [
            "population",
            "primary_networks"
        ]


class LanguageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LanguageForm, self).__init__(*args, **kwargs)
        self.fields["networks_translating"].widget.attrs["class"] = "select2-multiple"

    class Meta:
        model = Language
        fields = [
            "living_language",
            "gateway_dialect",
            "native_speakers",
            "networks_translating"
        ]


class ResourceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ResourceForm, self).__init__(*args, **kwargs)
        self.fields["copyright_holder"].widget.attrs["class"] = "select2-multiple"

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
