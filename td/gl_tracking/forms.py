from django import forms
from django.core.urlresolvers import reverse as urlReverse


class VariantSplitModalForm(forms.Form):
    template_name = "gl_tracking/variant_split_modal_form.html"
