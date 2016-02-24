from django import forms


class BSDateField(forms.DateField):
    description = "Bootstrap datepicker field"

    def __init__(self, *args, **kwargs):
        kwargs["widget"] = forms.DateInput(
            attrs={
                "class": "datepicker",
                "placeholder": "mm/dd/yyyy",
                "data-provide": "datepicker",
                "data-date-autoclose": "true",
                "data-date-keyboard-navigation": "false",
                "data-date-clear-btn": "true",
                "data-date-assume-nearby-year": "true",
                "data-date-start-date": "01/01/2000",
            },
            format="%m/%d/%Y",
        )
        if kwargs.get("input_formats") is None:
            kwargs["input_formats"] = [
                "%m-%d-%Y",
                "%m/%d/%Y",
            ]
        super(BSDateField, self).__init__(*args, **kwargs)


class LanguageCharField(forms.CharField):
    description = "Text field to search a language"

    def __init__(self, data_source_url="", css_class="language-selector", *args, **kwargs):
        kwargs["widget"] = forms.TextInput(
            attrs={
                "class": css_class,
                "data-source-url": data_source_url
            }
        )
        super(LanguageCharField, self).__init__(*args, **kwargs)
