from django import forms
from django.core.urlresolvers import reverse
from django.utils.formats import mark_safe
from django.utils import timezone
from django.forms.extras.widgets import SelectDateWidget

from td.models import Language
from .models import Charter, Event
from td.publishing.translations import OBSTranslation



class CharterForm(forms.ModelForm):

    # Modifying ModelForm's __init__()
    def __init__(self, *args, **kwargs):
        # Prevent ModelForm's __init__() from being thrown out completely
        super(CharterForm, self).__init__(*args, **kwargs)
        # The following will only ammend ModelForm's __init__() instead of replacing it
        # Overriding how 'language' shold be rendered
        self.fields['language'] = forms.CharField(
            widget = forms.TextInput(
                attrs = {
                    # Adding CSS class to the field
                    "class": "language-selector",
                    # 
                    "data-source-url": reverse("names_autocomplete")
                }
            ),
            required = True
        )

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

    def clean_language(self):
        lang_id = self.cleaned_data["language"]
        if lang_id:
            return Language.objects.get(pk=lang_id)

    def clean(self):
        cleaned_data = super(CharterForm, self).clean()
        lang = cleaned_data["language"]
        obs = OBSTranslation(base_path="", lang_code=lang.code)
        if not obs.qa_check():
            error_list_html = "".join(['<li><a href="{url}"><i class="fa fa-external-link"></i></a> {description}</li>'.format(**err) for err in obs.qa_issues_list])
            raise forms.ValidationError(mark_safe("The language does not pass the quality check for the following reasons: <ul>" + error_list_html + "</ul>"))
        return cleaned_data

    class Meta:
        model = Charter
        exclude = ['created_at', 'created_by']
        widgets = {
            # 'countries': forms.TextInput(),
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