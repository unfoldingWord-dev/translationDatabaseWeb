from django import forms
from .models import Charter, Event, Country


class CharterForm(forms.ModelForm):
	class Meta:
		model = Charter
		fields = [
			'target_lang_name',
			'target_lang_ietf',
			'gw_lang_name',
			'gw_lang_ietf',
			'countries',
			'name',
			'number',
			'start_date',
			'end_date',
			'lead_dept'
		]


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