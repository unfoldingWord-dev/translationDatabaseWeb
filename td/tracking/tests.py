import datetime
import logging
import unittest

from django.test import TestCase
from django.core.urlresolvers import reverse, resolve
from django.contrib.auth.models import User

from td.tracking.models import (
    Charter,
    Language,
    Department,
    Hardware,
    Software,
    TranslationService,
)

logger = logging.getLogger(__name__)
DEBUG = False


class ModelTestCase(TestCase):

    fixtures = ['td_tracking_seed.json']

    @unittest.skipIf(DEBUG, 'In DEBUG mode')
    def test_charter_string_representation(self):
        now = datetime.datetime.now()
        department = Department.objects.get(pk=1)
        language = Language.objects.create(code='wa')
        charter = Charter.objects.create(language=language, start_date=now, end_date=now, lead_dept=department)
        self.assertEqual(str(charter), 'wa')

    @unittest.skipIf(DEBUG, 'In DEBUG mode')
    def test_department_string_representation(self):
        department = Department.objects.create(name='Testing Services')
        self.assertEqual(str(department), 'Testing Services')

    @unittest.skipIf(DEBUG, 'In DEBUG mode')
    def test_hardware_string_representation(self):
        hardware = Hardware.objects.create(name='Test Hardware')
        self.assertEqual(str(hardware), 'Test Hardware')

    @unittest.skipIf(DEBUG, 'In DEBUG mode')
    def test_software_string_representation(self):
        software = Software.objects.create(name='Testing Software')
        self.assertEqual(str(software), 'Testing Software')

    @unittest.skipIf(DEBUG, 'In DEBUG mode')
    def test_translationService_string_representation(self):
        translationService = TranslationService.objects.create(name='Translation Service')
        self.assertEqual(str(translationService), 'Translation Service')


class ViewsTestCase(TestCase):

    fixtures = ['td_tracking_seed.json']

    def setUp(self):
        self.credentials = {'username': 'testuser', 'password': 'testpassword'}
        User.objects.create_user(**self.credentials)

    # Home

    @unittest.skipIf(DEBUG, 'In DEBUG mode')
    def test_home_view_success(self):
        response = self.client.get('/tracking/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<h1>Tracking Dashboard</h1>', response.content)

    # New Charter

    @unittest.skipIf(DEBUG, 'In DEBUG mode')
    def test_new_charter_view_no_login(self):
        response = self.client.get('/tracking/charter/new/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/account/login/?next=/tracking/charter/new/')

    @unittest.skipIf(DEBUG, 'In DEBUG mode')
    def test_new_charter_view_with_login(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/tracking/charter/new/', **self.credentials)
        self.assertEqual(response.status_code, 200)

    @unittest.skipIf(DEBUG, 'In DEBUG mode')
    def test_new_charter_view_with_param(self):
        response = self.client.get('/tracking/charter/new/99')
        self.assertEqual(response.status_code, 404)

    @unittest.skipIf(DEBUG, 'In DEBUG mode')
    def test_new_charter_view_correct_template(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/tracking/charter/new/', **self.credentials)
        self.assertIn('New Translation Project Charter', response.content)

    @unittest.skipIf(DEBUG, 'In DEBUG mode')
    def test_new_charter_view_default_start_date(self):
        date = datetime.datetime.now()
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/tracking/charter/new/', **self.credentials)
        month_option_string = '<option value="' + str(date.month) + '" selected="selected">'
        day_option_string = '<option value="' + str(date.day) + '" selected="selected">'
        year_option_string = '<option value="' + str(date.year) + '" selected="selected">'
        self.assertIn(month_option_string, response.content)
        self.assertIn(day_option_string, response.content)
        self.assertIn(year_option_string, response.content)

    @unittest.skipIf(DEBUG, 'In DEBUG mode')
    def test_new_charter_view_default_created_by(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/tracking/charter/new/', **self.credentials)
        created_by_string = 'name="created_by" type="hidden" value="testuser"'
        self.assertIn(created_by_string, response.content)

    # Update Charter

    @unittest.skipIf(DEBUG, 'In DEBUG mode')
    def test_charter_upadate_view_no_login(self):
        response = self.client.get('/tracking/charter/update/99/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/account/login/?next=/tracking/charter/update/99/')

    @unittest.skipIf(DEBUG, 'In DEBUG mode')
    def test_charter_upadate_view_with_login_not_found(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/tracking/charter/update/99/', **self.credentials)
        self.assertEqual(response.status_code, 404)

    @unittest.skipIf(DEBUG, 'In DEBUG mode')
    def test_charter_upadate_view_no_param(self):
        response = self.client.get('/tracking/charter/update/')
        self.assertEqual(response.status_code, 404)

    @unittest.skipIf(DEBUG, 'In DEBUG mode')
    def test_charter_update_view_correct_template(self):
        now = datetime.datetime.now()
        department = Department.objects.get(pk=1)
        language = Language.objects.create(code='wa')
        charter = Charter.objects.create(language=language, start_date=now, end_date=now, lead_dept=department)
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/tracking/charter/update/' + str(charter.id) + '/', **self.credentials)
        self.assertIn('Update Translation Project Charter', response.content)

    # Charter Detail

    @unittest.skipIf(DEBUG, 'In DEBUG mode')
    def test_charter_detail_page(self):

        response = self.client.get('/tracking/charter/detail/99')
        self.assertEqual(response.status_code, 301)

        response = self.client.get('/tracking/charter/detail/')
        self.assertEqual(response.status_code, 404)

    # Success

    @unittest.skipIf(DEBUG, 'In DEBUG mode')
    def test_success_with_no_login(self):

        response = self.client.get('/tracking/success/charter/99/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/account/login/?next=/tracking/success/charter/99/')

    @unittest.skipIf(DEBUG, 'In DEBUG mode')
    def test_success_with_login_no_referer(self):

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/tracking/success/charter/99/', **self.credentials)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/tracking/')

    @unittest.skipIf(DEBUG, 'In DEBUG mode')
    def test_success_with_login_wrong_referer(self):

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/tracking/success/charter/99/', username='testuser', password='testpassword', HTTP_REFERER='http://www.google.com')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/tracking/')

    @unittest.skipIf(DEBUG, 'In DEBUG mode')
    def test_success_with_login_correct_referer(self):

        now = datetime.datetime.now()
        department = Department.objects.get(pk=1)
        language = Language.objects.create(code='wa')
        charter = Charter.objects.create(language=language, start_date=now, end_date=now, lead_dept=department)
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/tracking/success/charter/' + str(charter.id) + '/', username='testuser', password='testpassword', HTTP_REFERER='http://td.unfoldingword.org/tracking/charter/new/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['link_id'] == str(charter.id))
        self.assertTrue(response.context['status'] == 'Success')
        self.assertIn('has been successfully added', response.context['message'])

    # test_success_with_login_correct_referer_wrong_type(self):


class UrlsTestCase(TestCase):

    @unittest.skipIf(DEBUG, 'In DEBUG mode')
    def test_url_reverse(self):
        url = reverse('tracking:project_list')
        self.assertEqual(url, '/tracking/')

        url = reverse('tracking:ajax_ds_charter_list')
        self.assertEqual(url, '/tracking/ajax/charters/')

        url = reverse('tracking:charter_add')
        self.assertEqual(url, '/tracking/charter/new/')

        url = reverse('tracking:charter', args=[999])
        self.assertEqual(url, '/tracking/charter/detail/999/')

        url = reverse('tracking:charter_update', args=[999])
        self.assertEqual(url, '/tracking/charter/update/999/')

        url = reverse('tracking:charter_add_success', kwargs={'obj_type': 'charter', 'pk': '999'})
        self.assertEqual(url, '/tracking/success/charter/999/')

    @unittest.skipIf(DEBUG, 'In DEBUG mode')
    def test_url_resolve_home(self):
        resolver = resolve('/tracking/')
        self.assertEqual(resolver.url_name, 'project_list')
        self.assertEqual(resolver.namespace, 'tracking')
        self.assertEqual(resolver.view_name, 'tracking:project_list')

    @unittest.skipIf(DEBUG, 'In DEBUG mode')
    def test_url_resolve_ajax_charters(self):
        resolver = resolve('/tracking/ajax/charters/')
        self.assertEqual(resolver.namespace, 'tracking')
        self.assertEqual(resolver.view_name, 'tracking:ajax_ds_charter_list')
        self.assertEqual(resolver.url_name, 'ajax_ds_charter_list')

    @unittest.skipIf(DEBUG, 'In DEBUG mode')
    def test_url_resolve_charter_new(self):
        resolver = resolve('/tracking/charter/new/')
        self.assertEqual(resolver.namespace, 'tracking')
        self.assertEqual(resolver.view_name, 'tracking:charter_add')
        self.assertEqual(resolver.url_name, 'charter_add')

    @unittest.skipIf(DEBUG, 'In DEBUG mode')
    def test_url_resolve_charter_add_success(self):
        resolver = resolve('/tracking/success/charter/999/')
        self.assertIn('pk', resolver.kwargs)
        self.assertIn('obj_type', resolver.kwargs)
        self.assertEqual(resolver.kwargs['pk'], '999')
        self.assertEqual(resolver.kwargs['obj_type'], 'charter')
        self.assertEqual(resolver.namespace, 'tracking')
        self.assertEqual(resolver.view_name, 'tracking:charter_add_success')
        self.assertEqual(resolver.url_name, 'charter_add_success')

    @unittest.skipIf(DEBUG, 'In DEBUG mode')
    def test_url_resolve_charter_update(self):
        resolver = resolve('/tracking/charter/update/999/')
        self.assertIn('pk', resolver.kwargs)
        self.assertEqual(resolver.kwargs['pk'], '999')
        self.assertEqual(resolver.namespace, 'tracking')
        self.assertEqual(resolver.view_name, 'tracking:charter_update')
        self.assertEqual(resolver.url_name, 'charter_update')

    @unittest.skipIf(DEBUG, 'In DEBUG mode')
    def test_url_resolve_charter_detail(self):
        resolver = resolve('/tracking/charter/detail/999/')
        self.assertIn('pk', resolver.kwargs)
        self.assertEqual(resolver.kwargs['pk'], '999')
        self.assertEqual(resolver.namespace, 'tracking')
        self.assertEqual(resolver.view_name, 'tracking:charter')
        self.assertEqual(resolver.url_name, 'charter')
