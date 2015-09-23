from django import forms
from django.core.urlresolvers import reverse as urlReverse
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import gettext as _
from django.utils.html import escape
# from django.utils.formats import mark_safe
# from django.utils import timezone

from td.models import Country, Language
from .models import (
    Charter,
    Department,
    Event,
    TranslationService,
    Hardware,
    Software,
    # Material,
    # Translator,
    # Facilitator,
)

import datetime


class MySelectDateWidget(SelectDateWidget):

    # Put Required=True on hold so the widget will include empty_label upon render
    def create_select(self, *args, **kwargs):
        old_state = self.is_required
        self.is_required = False
        result = super(MySelectDateWidget, self).create_select(*args, **kwargs)
        self.is_required = old_state
        return result


class CharterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CharterForm, self).__init__(*args, **kwargs)
        self.fields['countries'].queryset = Country.objects.order_by('name')
        self.fields['lead_dept'].queryset = Department.objects.order_by('name')
        self.fields['language'] = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    "class": "language-selector",
                    "data-source-url": urlReverse("names_autocomplete")
                }
            ),
            required=True
        )
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

    # def clean_number(self):
        # Validate the format of project (accounting) number

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        start_date = self.cleaned_data['start_date']
        if end_date <= start_date:
            raise forms.ValidationError(_('End date must be later than start date'), 'invalid_input')
        else:
            return end_date

    # Since a name can have unexpected characters, only check against empty
    def clean_contact_person(self):
        name = self.cleaned_data['contact_person']
        name = name.strip()
        if not name:
            raise forms.ValidationError(_('This field is required'), 'invalid_input')
        else:
            return escape(name)

    class Meta:
        model = Charter
        exclude = ['created_at']
        widgets = {
            'created_by': forms.HiddenInput(),
            'start_date': SelectDateWidget(
                attrs={'class': 'date-input'},
                years=range(datetime.datetime.now().year - 2, datetime.datetime.now().year + 11),
            ),
            'end_date': MySelectDateWidget(
                attrs={'class': 'date-input'},
                years=range(datetime.datetime.now().year - 2, datetime.datetime.now().year + 11),
            ),
        }


class EventForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['departments'].queryset = Department.objects.order_by('name')
        self.fields['hardware'].queryset = Hardware.objects.order_by('name')
        self.fields['software'].queryset = Software.objects.order_by('name')
        self.fields['translation_services'].queryset = TranslationService.objects.order_by('name')
        self.fields['charter'] = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    "class": "language-selector",
                    "data-source-url": urlReverse("tracking:charters_autocomplete")
                }
            ),
            required=True
        )
        if self.instance.pk:
            charter = self.instance.charter
            if charter:
                self.fields["charter"].widget.attrs["data-lang-pk"] = charter.id
                self.fields["charter"].widget.attrs["data-lang-ln"] = charter.language.ln
                self.fields["charter"].widget.attrs["data-lang-lc"] = charter.language.lc
                self.fields["charter"].widget.attrs["data-lang-lr"] = charter.language.lr
                self.fields["charter"].widget.attrs["data-lang-gl"] = charter.language.gateway_flag
        elif self.data.get("charter", None):
            try:
                charter = Charter.objects.get(pk=self.data["charter"])
                self.fields["charter"].widget.attrs["data-lang-pk"] = charter.id
                self.fields["charter"].widget.attrs["data-lang-ln"] = charter.language.ln
                self.fields["charter"].widget.attrs["data-lang-lc"] = charter.language.lc
                self.fields["charter"].widget.attrs["data-lang-lr"] = charter.language.lr
                self.fields["charter"].widget.attrs["data-lang-gl"] = charter.language.gateway_flag
            except:
                pass

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        start_date = self.cleaned_data['start_date']
        if end_date <= start_date:
            raise forms.ValidationError(_('End date must be later than start date'), 'invalid_input')
        else:
            return end_date

    def clean_contact_person(self):
        name = self.cleaned_data['contact_person']
        name = name.strip()
        if not name:
            raise forms.ValidationError(_('This field is required'), 'invalid_input')
        else:
            return name

    def clean_charter(self):
        number = int(self.cleaned_data['charter'])
        charter = Charter.objects.get(pk=number)
        return charter
    
    def process_facilitators(self, form_content):
        data = self.data
        for key in data:
            if key.startswith('facilitator') and key != 'facilitator-count':
                name = data[key]
                data[key] = name.strip()

    def _clean_fields(self):
        original_state = self.data._mutable
        self.data._mutable = True
        self.process_facilitators(self)
        self.data._mutable = original_state
        return super(EventForm, self)._clean_fields()

    class Meta:
        model = Event
        exclude = ['created_at']
        widgets = {
            'facilitators': forms.HiddenInput(),
            'created_by': forms.HiddenInput(),
            'start_date': SelectDateWidget(
                attrs={'class': 'date-input'},
                years=range(datetime.datetime.now().year - 2, datetime.datetime.now().year + 11),
            ),
            'end_date': MySelectDateWidget(
                attrs={'class': 'date-input'},
                years=range(datetime.datetime.now().year - 2, datetime.datetime.now().year + 11),
            ),
            'output_target': forms.Textarea(
                attrs={'rows': '3'}
            ),
            'publishing_process': forms.Textarea(
                attrs={'rows': '3'}
            ),
        }
