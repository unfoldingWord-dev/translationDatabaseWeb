from django import forms

from .models import Country, Language


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = [
            "population",
            "primary_denominations"
        ]


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = [
            "living_language",
            "gateway_dialect",
            "native_speakers",
            "denominations_translating"
        ]
