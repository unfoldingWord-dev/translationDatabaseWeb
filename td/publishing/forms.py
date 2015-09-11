from django import forms
from django.core.urlresolvers import reverse
from django.utils.formats import mark_safe

from multiupload.fields import MultiFileField

from td.models import Language
from .models import RecentCommunication, Connection, OfficialResource, PublishRequest
from .translations import OBSTranslation


class RecentComForm(forms.ModelForm):
    class Meta:
        model = RecentCommunication
        fields = ["communication"]
        widgets = {
            "communication": forms.Textarea(attrs={
                "class": "form-control",
                "cols": 40,
                "rows": 2
            }),
        }

    def __init__(self, *args, **kwargs):
        self.created_by = kwargs.pop("user")
        self.contact = kwargs.pop("contact")
        super(RecentComForm, self).__init__(*args, **kwargs)

    def save(self):
        entry = super(RecentComForm, self).save(commit=False)
        entry.created_by = self.created_by
        entry.contact = self.contact
        entry.save()


class ConnectionForm(forms.ModelForm):
    class Meta:
        model = Connection
        fields = ["con_dst", "con_type"]
        widgets = {
            "con_dst": forms.TextInput(attrs={
                "class": "form-control",
                "id": "contacts-id",
                "placeholder": "Add connection..."
            }),
        }

    def __init__(self, *args, **kwargs):
        self.contact = kwargs.pop("contact")
        super(ConnectionForm, self).__init__(*args, **kwargs)

    def save(self):
        entry = super(ConnectionForm, self).save(commit=False)
        entry.con_src = self.contact
        entry.save()
        if entry.con_type.mutual:
            Connection.objects.create(
                con_src=entry.con_dst,
                con_dst=self.contact,
                con_type=entry.con_type
            )


class OfficialResourceForm(forms.ModelForm):

    publish = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(OfficialResourceForm, self).__init__(*args, **kwargs)
        self.fields["language"] = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    "class": "language-selector",
                    "data-source-url": reverse("names_autocomplete")
                }
            ),
            required=True,
            label="Language"
        )
        if self.instance.pk is not None:
            if self.instance.language:
                lang = self.instance.language
                self.fields["language"].initial = lang.pk
                self.fields["language"].widget.attrs["data-lang-pk"] = lang.pk
                self.fields["language"].widget.attrs["data-lang-ln"] = lang.ln
                self.fields["language"].widget.attrs["data-lang-lc"] = lang.lc
                self.fields["language"].widget.attrs["data-lang-lr"] = lang.lr
        self.fields["source_text"].queryset = self.fields["source_text"].queryset.filter(official_resources__checking_level=3)
        if self.instance.publish_date:
            self.fields["publish"].initial = True
        if not self.fields["publish"].initial:
            self.fields["version"].widget.attrs["disabled"] = "disabled"
            self.fields["checking_entity"].widget.attrs["disabled"] = "disabled"
            self.fields["checking_level"].widget.attrs["disabled"] = "disabled"

    def clean_language(self):
        lang_id = self.cleaned_data["language"]
        if lang_id:
            return Language.objects.get(pk=lang_id)

    class Meta:
        model = OfficialResource
        fields = [
            "language",
            "resource_type",
            "contact",
            "date_started",
            "notes",
            "offline",
            "source_text",
            "source_version",
            "publish",
            "version",
            "checking_entity",
            "checking_level"
        ]


class PublishRequestForm(forms.ModelForm):

    license_agreements = MultiFileField(required=False, min_num=0, max_file_size=5242880)  # 5 MB

    def __init__(self, *args, **kwargs):
        super(PublishRequestForm, self).__init__(*args, **kwargs)
        self.fields["language"] = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    "class": "language-selector",
                    "data-source-url": reverse("names_autocomplete")
                }
            ),
            required=True
        )
        self.fields["source_text"].queryset = self.fields["source_text"].queryset.filter(official_resources__checking_level=3)

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
        cleaned_data = super(PublishRequestForm, self).clean()
        lang = cleaned_data["language"]
        obs = OBSTranslation(base_path="", lang_code=lang.code)
        if not obs.qa_check():
            error_list_html = "".join(['<li><a href="{url}"><i class="fa fa-external-link"></i></a> {description}</li>'.format(**err) for err in obs.qa_issues_list])
            raise forms.ValidationError(mark_safe("The language does not pass the quality check for the following reasons: <ul>" + error_list_html + "</ul>"))
        return cleaned_data

    class Meta:
        model = PublishRequest
        fields = [
            "requestor",
            "requestor_email",
            "resource_type",
            "language",
            "source_text",
            "source_version",
            "checking_level",
            "contributors",
            "license_agreements"
        ]
