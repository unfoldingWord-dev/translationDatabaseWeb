from django.test import TestCase

from td.tracking.models import (
	Department,
	Hardware,
	Software,
	TranslationService,
)


# class CharterModelTests(TestCase):

# 	def test_string_representation(self):
# 		charter = Charter.objects.create(

# 		)


class DepartmentModelTests(TestCase):

	def test_string_representation(self):
		department = Department.objects.create(name='Testing Services')
		self.assertEqual(str(department), 'Testing Services')


class HardwareModelTests(TestCase):

	def test_string_representation(self):
		hardware = Hardware.objects.create(name='Test Hardware')
		self.assertEqual(str(hardware), 'Test Hardware')


class SoftwareModelTests(TestCase):

	def test_string_representation(self):
		software = Software.objects.create(name='Testing Software')
		self.assertEqual(str(software), 'Testing Software')