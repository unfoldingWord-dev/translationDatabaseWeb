from django import forms
from django.core.exceptions import ValidationError

from td.models import Country
from td.fields import BSDateField

from .models import Progress, Partner


class VariantSplitModalForm(forms.Form):
    template_name = "gl_tracking/variant_split_modal_form.html"


class RegionAssignmentModalForm(forms.Form):
    template_name = "gl_tracking/region_assignment_modal_form.html"


class ProgressForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProgressForm, self).__init__(*args, **kwargs)
        self.fields["completion_date"] = BSDateField(required=False)

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
        self.fields["partner_start"] = BSDateField(required=False, label="Partnership Start Date")
        self.fields["partner_end"] = BSDateField(required=False, label="Partnership End Date")
        self.fields["country"].queryset = Country.objects.all().order_by("name")

    def clean_partner_end(self):
        partner_start = self.cleaned_data["partner_start"]
        partner_end = self.cleaned_data["partner_end"]
        if partner_start is not None and partner_end is not None and partner_start > partner_end:
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
        }
