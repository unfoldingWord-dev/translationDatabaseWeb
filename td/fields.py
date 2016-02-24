from django import forms


class BSDateField(forms.DateField):
    description = "Bootstrap datepicker field"

    def __init__(self, required=True, *args, **kwargs):
        kwargs["widget"] = forms.DateInput(
            attrs={
                "class": "datepicker",
                "placeholder": "mm/dd/yyyy",
            },
            format="%m/%d/%Y",
        )
        kwargs["input_formats"] = [
            "%Y-%m-%d",
            "%m-%d-%Y",
            "%Y/%m/%d",
            "%m/%d/%Y",
        ]
        kwargs["required"] = required
        super(BSDateField, self).__init__(*args, **kwargs)


class LanguageCharField(forms.CharField):
    description = "Text field to search a language"

    def __init__(self, data_source_url="", css_class="language-selector", required=True, *args, **kwargs):
        kwargs["widget"] = forms.TextInput(
            attrs={
                "class": css_class,
                "data-source-url": data_source_url
            }
        )
        kwargs["required"] = required
        super(LanguageCharField, self).__init__(*args, **kwargs)
