from django.db import models


LANG_NAMES = (
	('indonesian', 'Bahasa Indonesia'),
	('english', 'English (American)'),
	('british', 'English (British)'),
	('german', 'German'),
)

IETF_TAGS = (
	('ina', 'ina'),
	('eng', 'eng'),
	('bri', 'bri'),
	('deu', 'deu'),
)

OUTPUT_TARGETS = (
	('print', 'print'),
	('audio', 'audio'),
	('other', 'other'),
)

TRANSLATION_METHODS = (
	('lit', 'literal'),
	('dyn', 'dynamic'),
	('other', 'other'),
)

TECHNOLOGIES = (
	('btak', 'btak'),
	('tk', 'trasnlation keyboard'),
	('other', 'other'),
)

class Charter(models.Model):
	
	proj_num = models.SlugField(
		max_length = 50,
		primary_key = True,
	)

	lang_name = models.CharField(
		max_length = 200,
		choices = LANG_NAMES,
	)

	lang_ietf = models.SlugField(
		max_length = 50,
		choices = IETF_TAGS,
	)

	gw_lang_name = models.CharField(
		max_length = 50,
		choices = LANG_NAMES,
	)

	gw_lang_ietf = models.CharField(
		max_length = 50,
		choices = IETF_TAGS,
	)

	start_date = models.DateField(
	)

	end_date = models.DateField(
	)

	lead_dept = models.CharField(
		max_length = 200,
	)

	# lang_speaking_countries = *separate class?


class Event(models.Model):

	charter = models.ForeignKey(Charter)

	location = models.CharField(max_length = 200)

	start_date = models.DateField()

	end_date = models.DateField()

	lead_dept = models.CharField(max_length = 100)

	# materials = *separate class

	# translators = *separate class

	# facilitators = *separate class

	# supporting_networks = *separate class

	# supporting_depts = *separate class

	output_target = models.SlugField(max_length = 50)

	translation_method = models.SlugField(max_length = 50, choices = TRANSLATION_METHODS)

	tech_used = models.SlugField(max_length = 50, choices = TECHNOLOGIES)

	comp_tech_used = models.SlugField(max_length = 50)

	pub_process = models.TextField(max_length = 1500)

	follow_up = models.CharField(max_length = 50)


class Material(models.Model):
	
	event = models.ForeignKey(Event)

	name = models.CharField(max_length = 100)

	licensed = models.BooleanField(default = False)


class Translator(models.Model):

	event = models.ForeignKey(Event)

	name = models.CharField(max_length = 100)


class Facilitator(models.Model):

	event = models.ForeignKey(Event)

	name = models.CharField(max_length = 100)

	is_lead = models.BooleanField(default = False)

	speaks_gl = models.BooleanField(default = False)


class Network(models.Model):

	event = models.ForeignKey(Event)

	name = models.CharField(max_length = 200)


class Department(models.Model):

	event = models.ForeignKey(Event)

	name = models.CharField(max_length = 200)