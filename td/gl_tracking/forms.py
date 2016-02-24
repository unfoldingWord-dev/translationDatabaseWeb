from django import forms

from td.gl_tracking.models import Progress
from ..fields import BSDateField


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
