from django.test import TestCase
from td.tracking.models import Charter

import datetime
import logging
logger = logging.getLogger(__name__)

class CharterViewsTestCase(TestCase):
	fixtures = ['td_tracking_seed']

	@classmethod
	def setUpTestData(cls):
		cls.new = Charter.objects.create(
			language=1,
			countries=(1,2,3),
			start_date=datetime.datetime(2015, 01, 01, 13, 37),
			end_date=datetime.datetime(2017, 12, 30, 01, 01),
			number='L0123',
			lead_dept=1,
			contact_person='John Doe',
			created_at=datetime.datetime(2016, 01, 02, 03, 04),
			created_by='Vicky Leong',
		)

	def test_home_page(self):
		response = self.client.get('/tracking/')
		self.assertEqual(response.status_code, 200)

	def test_new_charter_page(self):
		response = self.client.get('/tracking/charter/new/')
		self.assertEqual(response.status_code, 200)

	def test_update_charter_page(self):
		response = self.client.get('/tracking/charter/update/')
		self.assertEqual(response.status_code, 404)

	def test_charter_detail_page(self):
		response = self.client.get('/tracking/charter/detail/')
		self.assertEqual(response.status_code, 404)

	def test_charter_add_success_page(self):
		response = self.client.get('/tracking/charter/new/sucess/')
		self.assertEqual(response.status_code, 404)