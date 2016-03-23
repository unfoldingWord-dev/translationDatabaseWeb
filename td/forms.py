from django import forms
from django.core.urlresolvers import reverse, reverse_lazy
from td.resources.forms import EntityTrackingForm
from .models import Network, Language, Country, TempLanguage


class TempLanguageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TempLanguageForm, self).__init__(*args, **kwargs)
        self.fields["common_name"].widget.attrs["class"] = "required"
        self.fields["direction"].widget.attrs["class"] = "required"
        self.fields["comment"].widget.attrs["rows"] = "4"

    class Meta:
        model = TempLanguage
        exclude = ["lang_assigned", "status", "status_comment", "source_name", "source_app"]
        labels = {
            "ietf_tag": "IETF tag",
            "common_name": "Common Name",
            "native_name": "Native Name",
        }


class NetworkForm(EntityTrackingForm):

    required_css_class = "required"

    class Meta:
        model = Network
        fields = [
            "name"
        ]


class CountryForm(EntityTrackingForm):
    required_css_class = "required"
    gl = forms.CharField(max_length=3)

    def clean_gl(self):
        pk = self.cleaned_data["gl"]
        if pk:
            return Language.objects.get(pk=pk).code

    def __init__(self, *args, **kwargs):
        super(CountryForm, self).__init__(*args, **kwargs)
        self.fields["primary_networks"].widget.attrs["class"] = "select2-multiple"
        self.fields["primary_networks"].help_text = ""
        self.fields["gl"] = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    "class": "language-selector",
                    "data-source-url": reverse("names_autocomplete")
                }
            ),
            required=False,
            label="Gateway Language"
        )
        if self.instance.pk is not None:
            if self.instance.gateway_language():
                lang = self.instance.gateway_language()
                self.fields["gl"].initial = lang.pk
                self.fields["gl"].widget.attrs["data-lang-pk"] = lang.pk
                self.fields["gl"].widget.attrs["data-lang-ln"] = lang.ln
                self.fields["gl"].widget.attrs["data-lang-lc"] = lang.lc
                self.fields["gl"].widget.attrs["data-lang-lr"] = lang.lr

    def save(self, commit=True):
        self.instance.extra_data.update({"gateway_language": self.cleaned_data["gl"]})
        return super(CountryForm, self).save(commit=commit)

    class Meta:
        model = Country
        fields = [
            "name",
            "region",
            "population",
            "primary_networks"
        ]


class LanguageForm(EntityTrackingForm):

    required_css_class = "required"

    def clean_gateway_language(self):
        pk = self.cleaned_data["gateway_language"]
        if pk:
            return Language.objects.get(pk=pk)

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
            lang = self.instance.gateway_language
            if lang:
                self.fields["gateway_language"].widget.attrs["data-lang-pk"] = lang.pk
                self.fields["gateway_language"].widget.attrs["data-lang-ln"] = lang.ln
                self.fields["gateway_language"].widget.attrs["data-lang-lc"] = lang.lc
                self.fields["gateway_language"].widget.attrs["data-lang-lr"] = lang.lr

    class Meta:
        model = Language
        fields = [
            "code",
            "iso_639_3",
            "name",
            "anglicized_name",
            "direction",
            "gateway_language",
            "native_speakers",
            "networks_translating"
        ]


class UploadGatewayForm(forms.Form):
    languages = forms.CharField(widget=forms.Textarea())
    required_css_class = "required"

    def clean_languages(self):
        lang_ids = [
            l.lower().strip() for l in self.cleaned_data["languages"].split("\n")
        ]
        errors = []
        for lid in lang_ids:
            try:
                Language.objects.get(code=lid)
            except Language.DoesNotExist:
                errors.append(lid)
        if errors:
            raise forms.ValidationError(
                "You entered some invalid language codes: {}".format(", ".join(errors))
            )
        return lang_ids
