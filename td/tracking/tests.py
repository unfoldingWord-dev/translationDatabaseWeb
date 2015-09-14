from django.test import TestCase
from django.core.urlresolvers import reverse, resolve

from td.tracking.models import (
    # Charter,
    # Language,
    # Country,
    Department,
    Hardware,
    Software,
    TranslationService,
)

# import datetime
import logging
logger = logging.getLogger(__name__)


class ModelTestCase(TestCase):

    def test_department_string_representation(self):
        department = Department.objects.create(name='Testing Services')
        self.assertEqual(str(department), 'Testing Services')

    def test_hardware_string_representation(self):
        hardware = Hardware.objects.create(name='Test Hardware')
        self.assertEqual(str(hardware), 'Test Hardware')

    def test_software_string_representation(self):
        software = Software.objects.create(name='Testing Software')
        self.assertEqual(str(software), 'Testing Software')

    def test_translationService_string_representation(self):
        translationService = TranslationService.objects.create(name='Translation Service')
        self.assertEqual(str(translationService), 'Translation Service')


class ViewsTestCase(TestCase):
    fixtures = ['td_tracking_seed']

    def test_request_home_page(self):
        response = self.client.get('/tracking/')
        self.assertEqual(response.status_code, 200)

    def test_request_new_charter_page(self):
        response = self.client.get('/tracking/charter/new/99')
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/tracking/charter/new/')
        self.assertEqual(response.status_code, 200)

    def test_request_update_charter_page(self):
        response = self.client.get('/tracking/charter/update/99')
        self.assertEqual(response.status_code, 301)

        response = self.client.get('/tracking/charter/update/')
        self.assertEqual(response.status_code, 404)

    def test_request_charter_detail_page(self):
        response = self.client.get('/tracking/charter/detail/99')
        self.assertEqual(response.status_code, 301)

        response = self.client.get('/tracking/charter/detail/')
        self.assertEqual(response.status_code, 404)

    def test_request_charter_add_success_page(self):
        response = self.client.get('/tracking/charter/new/success/99')
        self.assertEqual(response.status_code, 301)

        response = self.client.get('/tracking/charter/new/sucess/')
        self.assertEqual(response.status_code, 404)


class UrlsTestCase(TestCase):

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

        url = reverse('tracking:charter_add_success', args=[999])
        self.assertEqual(url, '/tracking/charter/new/success/999/')

    def test_url_resolve_home(self):
        resolver = resolve('/tracking/')
        self.assertEqual(resolver.url_name, 'project_list')
        self.assertEqual(resolver.namespace, 'tracking')
        self.assertEqual(resolver.view_name, 'tracking:project_list')

    def test_url_resolve_ajax_charters(self):
        resolver = resolve('/tracking/ajax/charters/')
        self.assertEqual(resolver.namespace, 'tracking')
        self.assertEqual(resolver.view_name, 'tracking:ajax_ds_charter_list')
        self.assertEqual(resolver.url_name, 'ajax_ds_charter_list')

    def test_url_resolve_charter_new(self):
        resolver = resolve('/tracking/charter/new/')
        self.assertEqual(resolver.namespace, 'tracking')
        self.assertEqual(resolver.view_name, 'tracking:charter_add')
        self.assertEqual(resolver.url_name, 'charter_add')

    def test_url_resolve_charter_add_success(self):
        resolver = resolve('/tracking/charter/new/success/999/')
        self.assertIn('pk', resolver.kwargs)
        self.assertEqual(resolver.kwargs['pk'], '999')
        self.assertEqual(resolver.namespace, 'tracking')
        self.assertEqual(resolver.view_name, 'tracking:charter_add_success')
        self.assertEqual(resolver.url_name, 'charter_add_success')

    def test_url_resolve_charter_update(self):
        resolver = resolve('/tracking/charter/update/999/')
        self.assertIn('pk', resolver.kwargs)
        self.assertEqual(resolver.kwargs['pk'], '999')
        self.assertEqual(resolver.namespace, 'tracking')
        self.assertEqual(resolver.view_name, 'tracking:charter_update')
        self.assertEqual(resolver.url_name, 'charter_update')

    def test_url_resolve_charter_detail(self):
        resolver = resolve('/tracking/charter/detail/999/')
        self.assertIn('pk', resolver.kwargs)
        self.assertEqual(resolver.kwargs['pk'], '999')
        self.assertEqual(resolver.namespace, 'tracking')
        self.assertEqual(resolver.view_name, 'tracking:charter')
        self.assertEqual(resolver.url_name, 'charter')
