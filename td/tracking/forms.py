from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.utils import timezone

from .models import Charter, Event



class CharterForm(forms.ModelForm):
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