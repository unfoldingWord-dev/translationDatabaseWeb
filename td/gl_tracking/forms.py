from django import forms
from td.gl_tracking.models import Progress
# from django.core.urlresolvers import reverse as urlReverse


class VariantSplitModalForm(forms.Form):
    template_name = "gl_tracking/variant_split_modal_form.html"


class ProgressForm(forms.ModelForm):

    class Meta:
        model = Progress
        exclude = ['language', 'type', 'created_by', 'created_at', 'modified_by', 'modified_at']
        widgets = {}
