from django import forms
from django.core.urlresolvers import reverse
from pinax.types.periods.fields import PeriodFormField
from pinax.types.periods import get_period, period_for_date
import datetime

from .models import (
    Country,
    Language,
    Network,
    Resource,
    Publisher,
    Title
)


class EntityTrackingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.source = kwargs.pop("source")
        super(EntityTrackingForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(EntityTrackingForm, self).save(commit=False)
        instance.source = self.source
        if commit:
            instance.save()
        return instance


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
            "direction",
            "gateway_language",
            "native_speakers",
            "networks_translating"
        ]


class TitleForm(forms.ModelForm):
    required_css_class = "required"

    class Meta:
        model = Title
        fields = [
            "name",
            "slug",
            "publisher"
        ]


class PublisherForm(forms.ModelForm):
    required_css_class = "required"

    class Meta:
        model = Publisher
        fields = [
            "name"
        ]


class ResourceForm(forms.ModelForm):
    required_css_class = "required"
    published_date = PeriodFormField(help_text="enter either a year or month/year or year-month", required=False)

    def __init__(self, *args, **kwargs):
        super(ResourceForm, self).__init__(*args, **kwargs)
        if self.instance.pk and self.instance.published_date:
            p_date = self.instance.published_date
            if p_date.month == 7 and p_date.day == 2:
                self.initial["published_date"] = get_period(period_for_date("yearly", date=p_date)).get_display()
            else:
                self.initial["published_date"] = get_period(period_for_date("monthly", date=p_date)).get_display()

    class Meta:
        model = Resource
        fields = [
            "title",
            "medias",
            "publisher",
            "published_flag",
            "published_date",
            "copyright_year",
            "extra_data"
        ]
        widgets = {
            "medias": forms.CheckboxSelectMultiple(attrs={"class": "multiple-checkbox"})
        }
        help_texts = {
            "publisher": "overrides the publisher set for the selected Title"
        }

    def clean_published_date(self):
        period_raw = self.cleaned_data["published_date"]
        if len(period_raw):
            p = get_period(period_raw)
            start_date, end_date = p.get_start_end()
            if p.is_period_type("yearly"):
                the_date = datetime.date(start_date.year, 7, 2)
            else:
                the_date = start_date
            return str(the_date)
        else:
            return ""


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
