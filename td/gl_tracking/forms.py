from django import forms
from td.gl_tracking.models import Progress


class VariantSplitModalForm(forms.Form):
    template_name = "gl_tracking/variant_split_modal_form.html"


class ProgressForm(forms.ModelForm):

    # Overriden add custom initialize the form
    def __init__(self, *args, **kwargs):
        super(ProgressForm, self).__init__(*args, **kwargs)
        print '\nSELF FIELDS', self.fields
        self.fields["completion_date"] = forms.DateField(
            widget=forms.DateInput(
                attrs={
                    "class": "datepicker",
                    "data-provide": "datepicker",
                    # "data-date-format": "",
                    "data-autoclose": "true",
                    "data-keyboard-navigation": "true",
                }
            ),
            input_formats=[
                "%Y-%m-%d",
                "%y-%m-%d",
                "%m-%d-%Y",
                "%m-%d-%y",
                "%Y/%m/%d",
                "%y/%m/%d",
                "%m/%d/%Y",
                "%m/%d/%y",
            ],
            required=False,
        )

    class Meta:
        model = Progress
        exclude = ['language', 'type', 'created_by', 'created_at', 'modified_by', 'modified_at', 'is_done']
        widgets = {
            "notes": forms.Textarea(attrs={"rows": "4"}),
            "methods": forms.CheckboxSelectMultiple(),
        }
