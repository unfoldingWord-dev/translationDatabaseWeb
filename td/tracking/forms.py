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

    # Overriden add custom initialize the form
    def __init__(self, *args, **kwargs):
        super(CharterForm, self).__init__(*args, **kwargs)
        # Alphabetize selections
        self.fields["countries"].queryset = Country.objects.order_by("name")
        self.fields["lead_dept"].queryset = Department.objects.order_by("name")
        # Add custom class and range of selection
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
        # Prep for jQuery select2 transformation
        self.fields["language"] = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    "class": "language-selector",
                    "data-source-url": urlReverse("names_autocomplete")
                }
            ),
            required=True
        )
        # Fill out the necessary attribute to display the selected language info
        #    if the form already has it.
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

    # Overriden to enforce date logic
    def clean_end_date(self):
        return check_end_date(self)

    # Overriden to trim spaces
    def clean_contact_person(self):
        return check_text_input(self, "contact_person")

    class Meta:
        model = Charter
        exclude = ["created_at"]
        widgets = {
            "created_by": forms.HiddenInput(),
        }


class MultiCharterForm(CharterForm):
     # Overriden add custom initialize the form
    def __init__(self, *args, **kwargs):
        super(MultiCharterForm, self).__init__(*args, **kwargs)
        # 
        self.fields["language"] = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    "class": "language-selector-marked",
                    "data-source-url": urlReverse("names_autocomplete")
                }
            ),
            required=True
        )

# --------------- #
#    EVENTFORM    #
# --------------- #


class EventForm(forms.ModelForm):

    # Overriden to add custom initialization
    # Argument pk is set to -1 by default
    def __init__(self, pk="-1", *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # Alphabetize items in selection
        self.fields["departments"].queryset = Department.objects.order_by("name")
        self.fields["hardware"].queryset = Hardware.objects.order_by("name")
        self.fields["software"].queryset = Software.objects.order_by("name")
        self.fields["translation_methods"].queryset = TranslationMethod.objects.order_by("name")
        self.fields["output_target"].queryset = Output.objects.order_by("name")
        self.fields["publication"].queryset = Publication.objects.order_by("name")
        # Add custom class and determine the range of selection
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
        # Prep charter field for jQuery select2 transformation
        # Preserve the "pk" arg in the element's data attr if there's any
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
        # Fill out the charter selection with necessary info if ...
        # ... the form is bound to a model ???
        if self.instance.pk:
            charter = self.instance.charter
            if charter:
                fill_search_charter(self, "charter", charter)
        # ... the form is posted back ...
        elif self.data.get("charter"):
            # Prioritize getting the charter "pk" from widget attribute
            pk = self.fields["charter"].widget.attrs["data-charter-pk"]
            if pk == "":
                pk = self.data.get("charter")
            try:
                charter = Charter.objects.get(pk=int(pk))
                fill_search_charter(self, "charter", charter)
            except Charter.DoesNotExist:
                # If there's no charter, there's nothing to do
                pass
        # ... the URL provides a "pk" arg.
        elif int(pk) >= 0:
            try:
                charter = Charter.objects.get(id=pk)
                fill_search_charter(self, "charter", charter)
            except Charter.DoesNotExist:
                # If there's no charter, there's nothing to do
                pass

    # Overriden to strip all custom fields
    def _clean_fields(self):
        original_state = self.data._mutable
        self.data._mutable = True
        for field in ["translator", "facilitator", "material"]:
            self.strip_custom_fields(self, field)
        self.data._mutable = original_state
        return super(EventForm, self)._clean_fields()

    # Overriden to return a charter instance
    def clean_charter(self):
        pk = self.fields["charter"].widget.attrs["data-charter-pk"]
        if pk == "":
            pk = self.cleaned_data["charter"]
        charter = Charter.objects.get(pk=int(pk))
        return charter

    # Overriden to enforce date logic
    def clean_end_date(self):
        end_date = check_end_date(self)
        return end_date

    # Overriden to trim spaces
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
            "number": forms.HiddenInput(),
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

    # Function: Assigned stripped strings to specified custom fields
    def strip_custom_fields(self, form, name):
        data = self.data
        for key in data:
            if key.startswith(name) and key != name + "-count":
                input = data[key]
                data[key] = input.strip()


# --------------------------- #
#    MULTICHARTEREVENTFORM    #
# --------------------------- #

# This form is only used one time by the MultiCharterEventView. It will subsequently be replaced
#    by MultiCharterEventForm1
class MultiCharterStarter(forms.Form):
    template_name = 'tracking/multi_charter_event_form.html'

    # Overriden to add custom initialization
    def __init__(self, *args, **kwargs):
        super(MultiCharterStarter, self).__init__(*args, **kwargs)
        # Add initial language field. This field's HTML name will be prefixed with "0-"
        #    by FormWizard and will be overriden by a new form in the MultiCharterEventView.
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


# This form will replace MultiCharterStarter on submit because it will be dynamically created by
#    the MultiCharterEventView based on how many charter/language fields the user adds/removes.
class MultiCharterEventForm1(forms.Form):
    template_name = 'tracking/multi_charter_event_form.html'

    # Overriden to add custom initialization
    def __init__(self, *args, **kwargs):
        super(MultiCharterEventForm1, self).__init__(*args, **kwargs)
        # self.fields will be a dictionary of names and CharField objects.
        #   ex: {"0-language_0": <CharField...>, "0-language_1": <CharField...>}
        for name, field in self.fields.iteritems():
            # Check for fields that have a value set from submission attempt
            if field.widget.attrs.get("value"):
                # Fill the input attrs with language info for select2 to display the correct info
                language = Language.objects.get(charter__pk=field.widget.attrs["value"])
                field.widget.attrs["data-lang-pk"] = language.id
                field.widget.attrs["data-lang-ln"] = language.ln
                field.widget.attrs["data-lang-lc"] = language.lc
                field.widget.attrs["data-lang-lr"] = language.lr
                field.widget.attrs["data-lang-gl"] = language.gateway_flag


class MultiCharterEventForm2(EventForm):

    # Overriding EventForm's custom initialization
    def __init__(self, *args, **kwargs):
        super(MultiCharterEventForm2, self).__init__(*args, **kwargs)
        # Since charter is not a part of this step, it's not required anymore
        self.fields["charter"] = forms.CharField(required=False)

    # Overridden EventForm's processing for charter field
    def clean_charter(self):
        # Since charter is not a part of this step, there's no need in validating it
        pass

    # Overriden EventForm's custom field validation
    def _clean_fields(self):
        # Notice we're not storing self.data._mutable in a temp var. For some reason,
        #    the program's complaining that self.data has no attr '_mutable'. But the
        #    below assigments on _mutable are still needed and work just fine.
        self.data._mutable = True
        for field in ["translator", "facilitator", "material"]:
            self.strip_custom_fields(self, field)
        self.data._mutable = False
        return super(EventForm, self)._clean_fields()

    # Overriden EvenForm's Meta class to adapt this form into MultiCharterEventView step 2
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


# Function: Assigns attributes for charter selector in EventForm
def fill_search_charter(form, field_name, object):
    form.fields[field_name].widget.attrs["data-charter-pk"] = object.id
    form.fields[field_name].widget.attrs["data-lang-pk"] = object.language.id
    form.fields[field_name].widget.attrs["data-lang-ln"] = object.language.ln
    form.fields[field_name].widget.attrs["data-lang-lc"] = object.language.lc
    form.fields[field_name].widget.attrs["data-lang-lr"] = object.language.lr
    form.fields[field_name].widget.attrs["data-lang-gl"] = object.language.gateway_flag
    form.fields[field_name].widget.attrs["value"] = object.language.id


# Function: Assigns attributes for language selector CharterForm
def fill_search_language(form, field_name, object):
    form.fields[field_name].widget.attrs["data-lang-pk"] = object.id
    form.fields[field_name].widget.attrs["data-lang-ln"] = object.ln
    form.fields[field_name].widget.attrs["data-lang-lc"] = object.lc
    form.fields[field_name].widget.attrs["data-lang-lr"] = object.lr
    form.fields[field_name].widget.attrs["data-lang-gl"] = object.gateway_flag


# Function: Raises error if start date is later than end date. Returns the end date.
def check_end_date(form):
    end_date = form.cleaned_data["end_date"]
    start_date = form.cleaned_data["start_date"]
    if end_date <= start_date:
        raise forms.ValidationError(_("End date must be later than start date"), "invalid_input")
    else:
        return end_date


# Function: Raises error if required fields contain empty string; Returns cleaned text
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


# Lets the form render empty value for required DateField
class MySelectDateWidget(SelectDateWidget):

    def create_select(self, *args, **kwargs):
        old_state = self.is_required
        self.is_required = False
        result = super(MySelectDateWidget, self).create_select(*args, **kwargs)
        self.is_required = old_state
        return result
