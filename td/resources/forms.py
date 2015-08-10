import datetime

from django import forms
from pinax.types.periods.fields import PeriodFormField
from pinax.types.periods import get_period, period_for_date

from .models import (
    Resource,
    Publisher,
    Title
)


class EntityTrackingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.source = kwargs.pop("source")
        super(EntityTrackingForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(EntityTrackingForm, self).save(commit=False)
        instance.source = self.source
        if commit:
            instance.save()
        return instance


class TitleForm(forms.ModelForm):
    required_css_class = "required"

    class Meta:
        model = Title
        fields = [
            "name",
            "slug",
            "publisher"
        ]


class PublisherForm(forms.ModelForm):
    required_css_class = "required"

    class Meta:
        model = Publisher
        fields = [
            "name"
        ]


class ResourceForm(forms.ModelForm):
    required_css_class = "required"
    published_date = PeriodFormField(help_text="enter either a year or month/year or year-month", required=False)

    def __init__(self, *args, **kwargs):
        super(ResourceForm, self).__init__(*args, **kwargs)
        if self.instance.pk and self.instance.published_date:
            p_date = self.instance.published_date
            if p_date.month == 7 and p_date.day == 2:
                self.initial["published_date"] = get_period(period_for_date("yearly", date=p_date)).get_display()
            else:
                self.initial["published_date"] = get_period(period_for_date("monthly", date=p_date)).get_display()

    class Meta:
        model = Resource
        fields = [
            "title",
            "medias",
            "publisher",
            "published_flag",
            "published_date",
            "copyright_year",
            "extra_data"
        ]
        widgets = {
            "medias": forms.CheckboxSelectMultiple(attrs={"class": "multiple-checkbox"})
        }
        help_texts = {
            "publisher": "overrides the publisher set for the selected Title"
        }

    def clean_published_date(self):
        period_raw = self.cleaned_data["published_date"]
        if len(period_raw):
            p = get_period(period_raw)
            start_date, end_date = p.get_start_end()
            if p.is_period_type("yearly"):
                the_date = datetime.date(start_date.year, 7, 2)
            else:
                the_date = start_date
            return str(the_date)
        else:
            return ""
