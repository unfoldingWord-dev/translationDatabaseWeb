from django import forms
from django.core.urlresolvers import reverse
from django.utils.formats import mark_safe

from multiupload.fields import MultiFileField

from td.models import Language
from td.publishing.models import (
    RecentCommunication, Connection, OfficialResource, PublishRequest)
from td.publishing.translations import TRANSLATION_TYPES


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

    def save(self, **kwargs):
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

    def save(self, **kwargs):
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

        if self.instance.publish_date:
            self.fields["publish"].initial = True

        if not self.fields["publish"].initial:
            self.fields["version"].widget.attrs["disabled"] = "disabled"
            self.fields["checking_entity"].widget.attrs["disabled"] = "disabled"
            self.fields["checking_level"].widget.attrs["disabled"] = "disabled"

        source_text_queryset = self.fields["source_text"].queryset.filter(
            official_resources__checking_level=3
        ).distinct("code")
        self.fields["source_text"].queryset = source_text_queryset

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

    # 5 MB limitation
    license_agreements = MultiFileField(
        required=False,
        min_num=0,
        max_file_size=5242880,
        label="License, Statement of Faith, and Translation Guidelines Agreements"
    )

    def __init__(self, *args, **kwargs):
        super(PublishRequestForm, self).__init__(*args, **kwargs)

        links = {
            'License Agreement': 'https://unfoldingword.org/license',
            'Statement of Faith': 'https://unfoldingword.org/faith',
            'Translation Guidelines': 'https://unfoldingword.org/guidelines'
        }

        help_links = []

        for key in links:
            help_links.append('<a href="' + links[key] + '" target="_blank">View ' + key + '</a><br>')

        self.fields["license_agreements"].help_text = '\r\n'.join(help_links)

        self.fields["language"] = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    "class": "language-selector",
                    "data-source-url": reverse("names_autocomplete")
                }
            ),
            required=True
        )

        source_text_queryset = self.fields["source_text"].queryset.filter(
            official_resources__checking_level=3
        ).distinct("code")
        self.fields["source_text"].queryset = source_text_queryset

        if self.instance.pk:
            lang = self.instance.language
            if lang:
                self.fields["language"].widget.attrs["data-lang-pk"] = lang.id
                self.fields["language"].widget.attrs["data-lang-ln"] = lang.ln
                self.fields["language"].widget.attrs["data-lang-lc"] = lang.lc
                self.fields["language"].widget.attrs["data-lang-lr"] = lang.lr
                self.fields["language"].widget.attrs["data-lang-gl"] = lang.gateway_flag
        elif self.data.get("language", None):
            # noinspection PyBroadException
            try:
                lang = Language.objects.get(pk=self.data["language"])
                self.fields["language"].widget.attrs["data-lang-pk"] = lang.id
                self.fields["language"].widget.attrs["data-lang-ln"] = lang.ln
                self.fields["language"].widget.attrs["data-lang-lc"] = lang.lc
                self.fields["language"].widget.attrs["data-lang-lr"] = lang.lr
                self.fields["language"].widget.attrs["data-lang-gl"] = lang.gateway_flag
            except:
                pass

        # these fields are not present when the user is creating a new publish request
        if 'rejected_at' in self.fields:
            self.fields['rejected_at'].widget.attrs['readonly'] = True
            self.fields['rejected_at'].widget.attrs['disabled'] = 'disabled'
            self.fields['rejected_by'].widget.attrs['readonly'] = True
            self.fields['rejected_by'].widget.attrs['disabled'] = 'disabled'

    def clean_language(self):
        lang_id = self.cleaned_data["language"]
        if lang_id:
            return Language.objects.get(pk=lang_id)

    def clean_rejected_at(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.rejected_at
        else:
            return None

    def clean_rejected_by(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.rejected_by
        else:
            return None

    def clean(self):
        cleaned_data = super(PublishRequestForm, self).clean()
        if self.is_valid():
            lang = cleaned_data["language"]
            resource_type = cleaned_data["resource_type"]
            resource_translator = TRANSLATION_TYPES.get(resource_type.short_name, None)
            if resource_translator:
                translation = resource_translator(base_path="", lang_code=lang.code)
                if not translation.qa_check():
                    error_list_html = "".join([
                        (
                            '<li><a href="{url}" target="_blank"><i class="fa '
                            'fa-external-link"></i></a> {description}</li>'
                        ).format(**err) for err in translation.qa_issues_list
                    ])
                    raise forms.ValidationError(mark_safe(
                        "This resource did not pass the quality check. Please "
                        "click each link below and fix the issue mentioned on "
                        "the Door43 site: <ul>" + error_list_html + "</ul>"
                    ))
        return cleaned_data

    class Meta:
        model = PublishRequest
        exclude = ["approved_at", "created_at", "requestor_email"]
        widgets = {"license_title": forms.TextInput()}


class PublishRequestNoAuthForm(PublishRequestForm):

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
