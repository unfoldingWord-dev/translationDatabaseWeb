import datetime

from django import forms
from django.core.urlresolvers import reverse as urlReverse
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import gettext as _
from django.utils.html import escape

from td.models import Country, Language
from .models import (
    Charter,
    Department,
    Network,
    Event,
    Hardware,
    Output,
    Publication,
    TranslationMethod,
    Software,
)

CHECKING_LEVEL = (
    ('', '---'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
)

# ----------------- #
#    CHARTERFORM    #
# ----------------- #


class CharterForm(forms.ModelForm):

    # Overwritten to customize the form
    def __init__(self, *args, **kwargs):
        super(CharterForm, self).__init__(*args, **kwargs)
        self.fields["countries"].queryset = Country.objects.order_by("name")
        self.fields["lead_dept"].queryset = Department.objects.order_by("name")
        self.fields["language"] = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    "class": "language-selector",
                    "data-source-url": urlReverse("names_autocomplete")
                }
            ),
            required=True
        )
        year = datetime.datetime.now().year
        self.fields["start_date"] = forms.DateField(
            widget=SelectDateWidget(
                years=range(year - 2, year + 10),
                attrs={"class": "date-input"}
            )
        )
        self.fields["end_date"] = forms.DateField(
            widget=MySelectDateWidget(
                years=range(year - 2, year + 10),
                attrs={"class": "date-input"}
            )
        )
        # Checking what?
        # Something to do with trying to create a duplicate charter.
        # Form says "undefined" if this is commented out.
        if self.instance.pk:
            lang = self.instance.language
            if lang:
                fill_search_language(self, "language", lang)
        elif self.data.get("language", None):
            try:
                lang = Language.objects.get(pk=self.data["language"])
                fill_search_language(self, "language", lang)
            except:
                pass

    # Overwritten to enforce date logic
    def clean_end_date(self):
        end_date = check_end_date(self)
        return end_date

    # Overwritten to trim spaces
    def clean_contact_person(self):
        name = check_text_input(self, "contact_person")
        return name

    class Meta:
        model = Charter
        exclude = ["created_at"]
        widgets = {
            "created_by": forms.HiddenInput(),
        }


# --------------- #
#    EVENTFORM    #
# --------------- #


class EventForm(forms.ModelForm):

    # Overwritten to customize the form
    def __init__(self, pk="-1", *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields["departments"].queryset = Department.objects.order_by("name")
        self.fields["hardware"].queryset = Hardware.objects.order_by("name")
        self.fields["software"].queryset = Software.objects.order_by("name")
        self.fields["translation_methods"].queryset = TranslationMethod.objects.order_by("name")
        self.fields["output_target"].queryset = Output.objects.order_by("name")
        self.fields["publication"].queryset = Publication.objects.order_by("name")
        self.fields["charter"] = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    "class": "language-selector",
                    "data-source-url": urlReverse("tracking:charters_autocomplete"),
                    "data-charter-pk": pk if pk != "-1" else ""
                }
            ),
            required=True
        )
        year = datetime.datetime.now().year
        self.fields["start_date"] = forms.DateField(
            widget=SelectDateWidget(
                years=range(year - 2, year + 10),
                attrs={"class": "date-input"}
            )
        )
        self.fields["end_date"] = forms.DateField(
            widget=MySelectDateWidget(
                years=range(year - 2, year + 10),
                attrs={"class": "date-input"}
            )
        )
        # Still not sure what this check does
        if self.instance.pk:
            charter = self.instance.charter
            if charter:
                fill_search_charter(self, "charter", charter)
        # If form is posted back...
        elif self.data.get("charter"):
            # Prioritize getting data from widget attribute
            pk = self.fields["charter"].widget.attrs["data-charter-pk"]
            if pk == "":
                pk = self.data.get("charter")
            try:
                charter = Charter.objects.get(pk=int(pk))
                fill_search_charter(self, "charter", charter)
            except Charter.DoesNotExist:
                pass
        # If the URL provides pk argument...
        elif int(pk) >= 0:
            try:
                charter = Charter.objects.get(id=pk)
                fill_search_charter(self, "charter", charter)
            except Charter.DoesNotExist:
                pass

    # Overwritten to strip all custom fields
    def _clean_fields(self):
        original_state = self.data._mutable
        self.data._mutable = True
        self.strip_custom_fields(self, "translator")
        self.strip_custom_fields(self, "facilitator")
        self.strip_custom_fields(self, "material")
        self.data._mutable = original_state
        return super(EventForm, self)._clean_fields()

    # Overwritten to return an object instance
    def clean_charter(self):
        pk = self.fields["charter"].widget.attrs["data-charter-pk"]
        if pk == "":
            pk = self.cleaned_data["charter"]
        charter = Charter.objects.get(pk=int(pk))
        return charter

    # Overwritten to enforce date logic
    def clean_end_date(self):
        end_date = check_end_date(self)
        return end_date

    # Overwritten to trim spaces
    def clean_contact_person(self):
        name = check_text_input(self, "contact_person")
        return name

    class Meta:
        model = Event
        exclude = ["created_at", "translators", "facilitators", "materials"]
        widgets = {
            "materials": forms.HiddenInput(),
            "facilitators": forms.HiddenInput(),
            "created_by": forms.HiddenInput(),
            "departments": forms.CheckboxSelectMultiple(),
            "publication": forms.CheckboxSelectMultiple(),
            "output_target": forms.CheckboxSelectMultiple(),
            "hardware": forms.CheckboxSelectMultiple(),
            "software": forms.CheckboxSelectMultiple(),
            "translation_methods": forms.CheckboxSelectMultiple(),
        }

    # -------------------------------- #
    #    CUSTOM EVENTFORM FUNCTIONS    #
    # -------------------------------- #

    # Function: Set stripped strings for specified custom fields
    def strip_custom_fields(self, form, name):
        data = self.data
        for key in data:
            if key.startswith(name) and key != name + "-count":
                input = data[key]
                data[key] = input.strip()


# --------------------------- #
#    MULTICHARTEREVENTFORM    #
# --------------------------- #


class MultiCharterStarter(forms.Form):
    template_name = 'tracking/multi_charter_event_form.html'

    def __init__(self, *args, **kwargs):
        super(MultiCharterStarter, self).__init__(*args, **kwargs)
        self.fields["language_0"] = forms.CharField(
            label="Charter",
            max_length=200,
            widget=forms.TextInput(
                attrs={
                    "class": "language-selector form-control",
                    "data-source-url": urlReverse("tracking:charters_autocomplete"),
                }
            ),
            required=True,
        )


class MultiCharterEventForm1(forms.Form):
    template_name = 'tracking/multi_charter_event_form.html'

    def __init__(self, *args, **kwargs):
        super(MultiCharterEventForm1, self).__init__(*args, **kwargs)
        # print '\nINIT MULTICHARTEREVENTFORM1'
        for name, field in self.fields.iteritems():
            if field.widget.attrs.get("value"):
                # print 'Value of', field, 'is', field.widget.attrs.get("value")
                language = Language.objects.get(charter__pk=field.widget.attrs["value"])
                field.widget.attrs["data-lang-pk"] = language.id
                field.widget.attrs["data-lang-ln"] = language.ln
                field.widget.attrs["data-lang-lc"] = language.lc
                field.widget.attrs["data-lang-lr"] = language.lr
                field.widget.attrs["data-lang-gl"] = language.gateway_flag
                # print 'Attrs of', field, 'are now', field.widget.attrs


class MultiCharterEventForm2(EventForm):

    def __init__(self, *args, **kwargs):
        super(MultiCharterEventForm2, self).__init__(*args, **kwargs)
        self.fields["charter"] = forms.CharField(required=False)

    def clean_charter(self):
        pass

    def _clean_fields(self):
        self.data._mutable = True
        self.strip_custom_fields(self, "translator")
        self.strip_custom_fields(self, "facilitator")
        self.strip_custom_fields(self, "material")
        self.data._mutable = False
        return super(EventForm, self)._clean_fields()

    class Meta:
        model = Event
        exclude = ["created_at", "created_by", "charter", "translators", "facilitators", "materials"]
        widgets = {
            "departments": forms.CheckboxSelectMultiple(),
            "publication": forms.CheckboxSelectMultiple(),
            "output_target": forms.CheckboxSelectMultiple(),
            "hardware": forms.CheckboxSelectMultiple(),
            "software": forms.CheckboxSelectMultiple(),
            "translation_methods": forms.CheckboxSelectMultiple(),
        }


# ---------------------- #
#    COMMON FUNCTIONS    #
# ---------------------- #


# Function: Assign attributes for charter selector
def fill_search_charter(form, field_name, object):
    form.fields[field_name].widget.attrs["data-charter-pk"] = object.id
    form.fields[field_name].widget.attrs["data-lang-pk"] = object.language.id
    form.fields[field_name].widget.attrs["data-lang-ln"] = object.language.ln
    form.fields[field_name].widget.attrs["data-lang-lc"] = object.language.lc
    form.fields[field_name].widget.attrs["data-lang-lr"] = object.language.lr
    form.fields[field_name].widget.attrs["data-lang-gl"] = object.language.gateway_flag
    form.fields[field_name].widget.attrs["value"] = object.language.id


# Function: Assign attributes for language selector
def fill_search_language(form, field_name, object):
    form.fields[field_name].widget.attrs["data-lang-pk"] = object.id
    form.fields[field_name].widget.attrs["data-lang-ln"] = object.ln
    form.fields[field_name].widget.attrs["data-lang-lc"] = object.lc
    form.fields[field_name].widget.attrs["data-lang-lr"] = object.lr
    form.fields[field_name].widget.attrs["data-lang-gl"] = object.gateway_flag


# Function: Raise error if start date is later than end date. Returns the end date.
def check_end_date(form):
    end_date = form.cleaned_data["end_date"]
    start_date = form.cleaned_data["start_date"]
    if end_date <= start_date:
        raise forms.ValidationError(_("End date must be later than start date"), "invalid_input")
    else:
        return end_date


# Function: Raise error if required fields contain empty string; Returns cleaned text
def check_text_input(form, field_name):
    text = form.cleaned_data[field_name]
    text = text.strip()
    if not text:
        raise forms.ValidationError(_("This field is required"), "invalid_input")
    else:
        return escape(text)


# ------------------- #
#    CUSTOM WIDGET    #
# ------------------- #


# Let the form render empty value for required DateField
class MySelectDateWidget(SelectDateWidget):

    def create_select(self, *args, **kwargs):
        old_state = self.is_required
        self.is_required = False
        result = super(MySelectDateWidget, self).create_select(*args, **kwargs)
        self.is_required = old_state
        return result
