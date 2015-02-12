from django import forms
from django.core.urlresolvers import reverse

#from td.models import Language as SourceLanguage
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

    required_css_class = "required"

    class Meta:
        model = Network
        fields = [
            "name"
        ]


class CountryForm(forms.ModelForm):

    required_css_class = "required"

    def __init__(self, *args, **kwargs):
        super(CountryForm, self).__init__(*args, **kwargs)
        self.fields["primary_networks"].widget.attrs["class"] = "select2-multiple"
        self.fields["primary_networks"].help_text = ""

    class Meta:
        model = Country
        fields = [
            "code",
            "name",
            "area",
            "population",
            "primary_networks"
        ]


class LanguageForm(forms.ModelForm):

    required_css_class = "required"

    def clean_gateway_language(self):
        code = self.cleaned_data["gateway_dialect"]
        if code:
            return Language.objects.get(code=code)

    def __init__(self, *args, **kwargs):
        super(LanguageForm, self).__init__(*args, **kwargs)
        self.fields["networks_translating"].widget.attrs["class"] = "select2-multiple"
        self.fields["networks_translating"].help_text = ""
        self.fields["gateway_language"] = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    "class": "language-selector",
                    "data-source-url": reverse("names_autocomplete")
                }
            ),
            required=False
        )
        if self.instance.pk is not None:
            #self.initial.update({
            #    "living_language": self.instance.living_language.code,
            #    "gateway_dialect": self.instance.gateway_dialect.code if self.instance.gateway_dialect else ""
            #})
            #lang = self.instance.living_language
            lang = self.instance.gateway_language
            if lang:
                self.fields["gateway_dialect"].widget.attrs["data-lang-ln"] = lang.ln
                self.fields["gateway_dialect"].widget.attrs["data-lang-lc"] = lang.lc
                self.fields["gateway_dialect"].widget.attrs["data-lang-lr"] = lang.lr

    class Meta:
        model = Language
        fields = [
            "code",
            "name",
            "gateway_language",
            "native_speakers",
            "networks_translating"
        ]


class ResourceForm(forms.ModelForm):

    required_css_class = "required"

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

    required_css_class = "required"

    def __init__(self, *args, **kwargs):
        self.language = kwargs.pop("language")
        super(ScriptureForm, self).__init__(*args, **kwargs)
        self.fields["kind"].widget = forms.RadioSelect(choices=self.fields["kind"].widget.choices)
        self.fields["bible_content"].widget.attrs["class"] = "select2-multiple"
        self.fields["wip"].queryset = self.fields["wip"].queryset.filter(language=self.language)

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

    required_css_class = "required"

    class Meta:
        model = TranslationNeed
        fields = [
            "text_gaps",
            "text_updates",
            "other_gaps",
            "other_updates"
        ]


class WorkInProgressForm(forms.ModelForm):

    required_css_class = "required"

    def __init__(self, *args, **kwargs):
        super(WorkInProgressForm, self).__init__(*args, **kwargs)
        self.fields["kind"].widget = forms.RadioSelect(choices=self.fields["kind"].widget.choices)
        self.fields["paradigm"].widget = forms.RadioSelect(choices=self.fields["paradigm"].widget.choices)
        self.fields["bible_content"].widget.attrs["class"] = "select2-multiple"
        self.fields["translators"].widget.attrs["class"] = "select2-multiple"
        self.fields["anticipated_completion_date"].widget.attrs["class"] = "date-picker"

    class Meta:
        model = WorkInProgress
        fields = [
            "kind",
            "bible_content",
            "paradigm",
            "translators",
            "anticipated_completion_date"
        ]
