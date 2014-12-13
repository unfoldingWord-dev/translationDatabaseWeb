from django import forms
from django.core.urlresolvers import reverse

from td.models import Language as SourceLanguage
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

    def clean_living_language(self):
        code = self.cleaned_data["living_language"]
        return SourceLanguage.objects.get(code=code)

    def clean_gateway_dialect(self):
        code = self.cleaned_data["gateway_dialect"]
        return SourceLanguage.objects.get(code=code)

    def __init__(self, *args, **kwargs):
        super(LanguageForm, self).__init__(*args, **kwargs)
        self.fields["networks_translating"].widget.attrs["class"] = "select2-multiple"
        self.fields["living_language"] = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    "class": "language-selector",
                    "data-source-url": reverse("names_autocomplete")
                }
            )
        )
        self.fields["gateway_dialect"] = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    "class": "language-selector",
                    "data-source-url": reverse("names_autocomplete")
                }
            )
        )
        self.initial.update({
            "living_language": self.instance.living_language.code if self.instance.living_language else "",
            "gateway_dialect": self.instance.gateway_dialect.code if self.instance.gateway_dialect else ""
        })
        if self.instance.living_language is not None:
            lang = self.instance.living_language
            self.fields["living_language"].widget.attrs["data-lang-ln"] = lang.ln
            self.fields["living_language"].widget.attrs["data-lang-lc"] = lang.lc
            self.fields["living_language"].widget.attrs["data-lang-lr"] = lang.lr
        if self.instance.gateway_dialect is not None:
            lang = self.instance.gateway_dialect
            self.fields["gateway_dialect"].widget.attrs["data-lang-ln"] = lang.ln
            self.fields["gateway_dialect"].widget.attrs["data-lang-lc"] = lang.lc
            self.fields["gateway_dialect"].widget.attrs["data-lang-lr"] = lang.lr

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

    def __init__(self, *args, **kwargs):
        super(ScriptureForm, self).__init__(*args, **kwargs)
        self.fields["kind"].widget = forms.RadioSelect(choices=self.fields["kind"].widget.choices)
        self.fields["bible_content"].widget.attrs["class"] = "select2-multiple"

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

    def __init__(self, *args, **kwargs):
        super(WorkInProgressForm, self).__init__(*args, **kwargs)
        self.fields["kind"].widget = forms.RadioSelect(choices=self.fields["kind"].widget.choices)
        self.fields["paradigm"].widget = forms.RadioSelect(choices=self.fields["paradigm"].widget.choices)
        self.fields["bible_content"].widget.attrs["class"] = "select2-multiple"
        self.fields["translators"].widget.attrs["class"] = "select2-multiple"

    class Meta:
        model = WorkInProgress
        fields = [
            "kind",
            "bible_content",
            "paradigm",
            "translators",
            "anticipated_completion_date"
        ]
