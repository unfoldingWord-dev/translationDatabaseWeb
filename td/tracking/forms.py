from django import forms
from django.core.urlresolvers import reverse as urlReverse
from django.utils.formats import mark_safe
from django.utils import timezone
from django.utils.translation import gettext as _
from django.forms.extras.widgets import SelectDateWidget

from td.models import Language, Country
from .models import Charter, Event
from td.publishing.translations import OBSTranslation

import re



class CharterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CharterForm, self).__init__(*args, **kwargs)
        self.fields['language'] = forms.CharField(
            widget = forms.TextInput(
                attrs = {
                    "class": "language-selector",
                    "data-source-url": urlReverse("names_autocomplete")
                }
            ),
            required = True
        )
        self.fields['countries'].queryset = Country.objects.order_by('name')

        # Checking what?
        # Something to do with trying to create a duplicate charter.
        # Form says "undefined" if this is commented out.
        if self.instance.pk:
            lang = self.instance.language
            if lang:
                self.fields["language"].widget.attrs["data-lang-pk"] = lang.id
                self.fields["language"].widget.attrs["data-lang-ln"] = lang.ln
                self.fields["language"].widget.attrs["data-lang-lc"] = lang.lc
                self.fields["language"].widget.attrs["data-lang-lr"] = lang.lr
                self.fields["language"].widget.attrs["data-lang-gl"] = lang.gateway_flag
        elif self.data.get("language", None):
            try:
                lang = Language.objects.get(pk=self.data["language"])
                self.fields["language"].widget.attrs["data-lang-pk"] = lang.id
                self.fields["language"].widget.attrs["data-lang-ln"] = lang.ln
                self.fields["language"].widget.attrs["data-lang-lc"] = lang.lc
                self.fields["language"].widget.attrs["data-lang-lr"] = lang.lr
                self.fields["language"].widget.attrs["data-lang-gl"] = lang.gateway_flag
            except:
                pass

    def clean_contact_person(self):
        number = self.cleaned_data['number'].strip()
        v = re.compile('[0-9a-z.-]+', re.IGNORECASE)
        if not v.match(number):
            raise forms.ValidationError(_('Use only letters, numbers, hyphens, or periods'), 'invalid_input')
        return number

    def clean_contact_person(self):
        name = self.cleaned_data['contact_person']
        name = name.strip()
        v = re.compile('[a-z ]+', re.IGNORECASE)
        if not v.match(name):
            raise forms.ValidationError(_('Use only letters and spaces'), 'invalid_input')
        return name

    class Meta:
        model = Charter
        exclude = ['created_at']
        widgets = {
            'created_by': forms.HiddenInput(),
            'start_date': SelectDateWidget(
                attrs = {'class': 'date-input'}
            ),
            'end_date': SelectDateWidget(
                attrs = {'class': 'date-input'}
            ),
        }
        


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'charter',
            'location',
            'start_date',
            'end_date',
            'lead_dept',
            'materials',
            'translators',
            'facilitators',
            'output_target',
            'translation_method',
            'tech_used',
            'comp_tech_used',
            'networks',
            'departments',
            'pub_process',
            'follow_up'
        ]