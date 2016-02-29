from django import forms
from django.core.exceptions import ValidationError
from td.gl_tracking.models import Progress, Partner
from td.models import Country


class VariantSplitModalForm(forms.Form):
    template_name = "gl_tracking/variant_split_modal_form.html"


class RegionAssignmentModalForm(forms.Form):
    template_name = "gl_tracking/region_assignment_modal_form.html"


class ProgressForm(forms.ModelForm):

    # Overriden add custom initialize the form
    def __init__(self, *args, **kwargs):
        super(ProgressForm, self).__init__(*args, **kwargs)
        self.fields["completion_date"] = forms.DateField(
            widget=forms.DateInput(
                attrs={
                    "class": "datepicker",
                    "data-provide": "datepicker",
                    "data-autoclose": "true",
                    "data-keyboard-navigation": "true",
                }
            ),
            input_formats=[
                "%Y-%m-%d",
                "%m-%d-%Y",
                "%Y/%m/%d",
                "%m/%d/%Y",
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


class PartnerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PartnerForm, self).__init__(*args, **kwargs)
        self.fields["partner_start"] = forms.DateField(
            widget=forms.DateInput(
                attrs={
                    "class": "datepicker",
                    "data-provide": "datepicker",
                    "data-autoclose": "true",
                    "data-keyboard-navigation": "true",
                },
                format="%m/%d/%Y",
            ),
            input_formats=[
                "%m/%d/%Y",
            ],
            required=False,
        )
        self.fields["partner_end"] = forms.DateField(
            widget=forms.DateInput(
                attrs={
                    "class": "datepicker",
                    "data-provide": "datepicker",
                    "data-autoclose": "true",
                    "data-keyboard-navigation": "true",
                },
                format="%m/%d/%Y",
            ),
            input_formats=[
                "%m/%d/%Y",
            ],
            required=False,
        )
        self.fields["country"].queryset = Country.objects.all().order_by("name")

    def clean_partner_end(self):
        partner_start = self.cleaned_data["partner_start"]
        partner_end = self.cleaned_data["partner_end"]
        if partner_start is not None and partner_start > partner_end:
            raise ValidationError("Partner end must be after partner start")
        return partner_end

    class Meta:
        model = Partner
        fields = "__all__"
        labels = {
            "contact_phone": "Contact Phone Number",
            "contact_email": "Contact Email",
            "province": "State/Region",
            "is_active": "Active Partner",
            "contact_name": "Contact Name",
            "partner_start": "Partner Start",
            "partner_end": "Partner End"
        }
