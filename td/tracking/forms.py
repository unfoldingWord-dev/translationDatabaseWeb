from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.utils import timezone
from django.utils.formats import mark_safe
from django.core.urlresolvers import reverse

from td.models import Language
from td.publishing.translations import OBSTranslation
from .models import Charter, Event



class CharterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CharterForm, self).__init__(*args, **kwargs)
        self.fields['language'] = forms.CharField(
            widget = forms.TextInput(
                attrs = {
                    "class": "language-selector",
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
            'countries': forms.TextInput(),
            'start_date': SelectDateWidget(),
            'end_date': SelectDateWidget(),
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