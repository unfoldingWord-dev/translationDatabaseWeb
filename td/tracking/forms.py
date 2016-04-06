from django import forms
from django.core.urlresolvers import reverse as urlReverse
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import gettext as _
from django.utils.html import escape

from td.models import Language
from td.gl_tracking.models import Partner
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
from ..fields import BSDateField, LanguageCharField

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

    def __init__(self, *args, **kwargs):
        super(CharterForm, self).__init__(*args, **kwargs)
        self.fields["lead_dept"].queryset = Department.objects.order_by("name")
        self.fields["partner"].queryset = Partner.objects.order_by("name")
        self.fields["start_date"] = BSDateField()
        self.fields["end_date"] = BSDateField()
        self.fields["language"] = LanguageCharField(urlReverse("names_autocomplete"))
        # Fill out the necessary attribute to display the selected language info
        #    if the form already has it.
        try:
            lang = None
            if self.instance.pk:
                lang = self.instance.language
            elif self.data.get("language", None):
                lang = Language.objects.get(pk=self.data["language"])
            elif kwargs.get("initial") is not None and kwargs["initial"].get("language") is not None:
                lang = Language.objects.get(pk=kwargs["initial"]["language"])
            fill_search_language(self, "language", lang)
        except Language.DoesNotExist:
            pass

    def clean_end_date(self):
        return check_end_date(self.cleaned_data)

    def clean_contact_person(self):
        return check_text_input(self, "contact_person")

    class Meta:
        model = Charter
        exclude = ["created_at", "modified_at", "countries", "number"]
        widgets = {
            "created_by": forms.HiddenInput(),
            "modified_by": forms.HiddenInput(),
            "countries": forms.SelectMultiple(attrs={"size": "8"})
        }


class MultiCharterForm(CharterForm):

    def __init__(self, *args, **kwargs):
        super(MultiCharterForm, self).__init__(*args, **kwargs)
        self.fields["language"] = LanguageCharField(urlReverse("names_autocomplete"), "language-selector-marked")

    def has_changed(self):
        changed_data = super(MultiCharterForm, self).has_changed()
        return bool(self.initial or changed_data)


# --------------- #
#    EVENTFORM    #
# --------------- #


class EventForm(forms.ModelForm):

    def __init__(self, pk="-1", *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields = determine_widget(self.fields, ["departments", "hardware", "software", "translation_methods",
                                                     "output_target", "publication"], 9)
        self.fields["departments"].queryset = Department.objects.order_by("name")
        self.fields["hardware"].queryset = Hardware.objects.order_by("name")
        self.fields["software"].queryset = Software.objects.order_by("name")
        self.fields["translation_methods"].queryset = TranslationMethod.objects.order_by("name")
        self.fields["output_target"].queryset = Output.objects.order_by("name")
        self.fields["publication"].queryset = Publication.objects.order_by("name")
        self.fields["partner"].queryset = Partner.objects.order_by("name")
        self.fields["start_date"] = BSDateField()
        self.fields["end_date"] = BSDateField()
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

    # Overridden to strip all custom fields
    def _clean_fields(self):
        original_state = self.data._mutable
        self.data._mutable = True
        for field in ["translator", "facilitator", "material"]:
            self.strip_custom_fields(self, field)
        self.data._mutable = original_state
        return super(EventForm, self)._clean_fields()

    # Overridden to return a charter instance
    def clean_charter(self):
        pk = self.fields["charter"].widget.attrs["data-charter-pk"]
        if pk == "":
            pk = self.cleaned_data["charter"]
        charter = Charter.objects.get(pk=int(pk))
        return charter

    # Overridden to enforce date logic
    def clean_end_date(self):
        return check_end_date(self.cleaned_data)

    # Overridden to trim spaces
    def clean_contact_person(self):
        name = check_text_input(self, "contact_person")
        return name

    class Meta:
        model = Event
        exclude = ["created_at", "modified_at", "translators", "facilitators", "materials"]
        widgets = {
            "created_by": forms.HiddenInput(),
            "modified_by": forms.HiddenInput(),
            "materials": forms.HiddenInput(),
            "facilitators": forms.HiddenInput(),
            "number": forms.HiddenInput(),
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

    # Overridden to add custom initialization
    def __init__(self, *args, **kwargs):
        super(MultiCharterStarter, self).__init__(*args, **kwargs)
        # Add initial language field. This field's HTML name will be prefixed with "0-"
        #    by FormWizard and will be overriden by a new form in the MultiCharterEventView.
        self.fields["language_0"] = forms.CharField(
            label="Charter",
            max_length=200,
            widget=forms.TextInput(
                attrs={
                    "class": "language-selector-marked form-control",
                    "data-source-url": urlReverse("tracking:charters_autocomplete"),
                }
            ),
            required=True,
        )


# This form will replace MultiCharterStarter on submit because it will be dynamically created by
#    the MultiCharterEventView based on how many charter/language fields the user adds/removes.
class MultiCharterEventForm1(forms.Form):
    template_name = 'tracking/multi_charter_event_form.html'

    # Overridden to add custom initialization
    def __init__(self, *args, **kwargs):
        super(MultiCharterEventForm1, self).__init__(*args, **kwargs)
        # self.fields will be a dictionary of names and CharField objects.
        #   ex: {"0-language_0": <CharField...>, "0-language_1": <CharField...>}
        for name, field in self.fields.iteritems():
            # Check for fields that have a value set from submission attempt
            if field.widget.attrs.get("value", None):
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

    # Overridden EventForm's custom field validation
    def _clean_fields(self):
        # Notice we're not storing self.data._mutable in a temp var. For some reason,
        #    the program's complaining that self.data has no attr '_mutable'. But the
        #    below assigments on _mutable are still needed and work just fine.
        self.data._mutable = True
        for field in ["translator", "facilitator", "material"]:
            self.strip_custom_fields(self, field)
        self.data._mutable = False
        return super(EventForm, self)._clean_fields()

    # Overridden EvenForm's Meta class to adapt this form into MultiCharterEventView step 2
    class Meta:
        model = Event
        exclude = ["created_at", "created_by", "modified_at", "modified_by", "charter", "translators", "facilitators", "materials"]
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
    if object is not None:
        form.fields[field_name].widget.attrs["data-lang-pk"] = object.id
        form.fields[field_name].widget.attrs["data-lang-ln"] = object.ln
        form.fields[field_name].widget.attrs["data-lang-lc"] = object.lc
        form.fields[field_name].widget.attrs["data-lang-lr"] = object.lr
        form.fields[field_name].widget.attrs["data-lang-gl"] = object.gateway_flag


# Function: Raises error if start date is later than end date. Returns the end date.
def check_end_date(cleaned_data):
    start_date = cleaned_data.get("start_date")
    end_date = cleaned_data.get("end_date")
    if not start_date:
        raise forms.ValidationError(_("Start date is required"), "invalid_input")
    if end_date <= start_date:
        raise forms.ValidationError(_("End date must be later than start date"), "invalid_input")
    return end_date


# Function: Raises error if required fields contain empty string; Returns cleaned text
def check_text_input(form, field_name):
    text = form.cleaned_data[field_name]
    text = text.strip()
    if not text:
        raise forms.ValidationError(_("This field is required"), "invalid_input")
    else:
        return escape(text)


# Function:
def determine_widget(fields, names, limit):
    """
    Determine what widget should be used based on the given limit.
    This is used mainly for deciding whether a field should be displayed as checkboxes
       or as a multiselect (if it's too long).
    """
    for name in names:
        fields[name].widget = forms.SelectMultiple() if len(fields[name].queryset) > limit else forms.CheckboxSelectMultiple()
    return fields


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
