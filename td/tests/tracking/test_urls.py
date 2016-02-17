from django.test import TestCase
from django.core.urlresolvers import reverse


class urlPatternsTestCase(TestCase):

    def test_home_url_reverse(self):
        url = reverse("tracking:project_list")
        self.assertEqual(url, "/tracking/")

    def test_charter_url_reverse(self):
        url = reverse("tracking:charter_add")
        self.assertEqual(url, "/tracking/charter/new/")
        url = reverse("tracking:charter_update", args=[9999])
        self.assertEqual(url, "/tracking/charter/update/9999/")
        url = reverse("tracking:multi_charter_add")
        self.assertEqual(url, "/tracking/mc/new/")

    def test_event_url_reverse(self):
        url = reverse("tracking:event_add")
        self.assertEqual(url, "/tracking/event/new/")
        url = reverse("tracking:event_add_specific", args=[9999])
        self.assertEqual(url, "/tracking/event/new/9999/")
        url = reverse("tracking:event_update", args=[9999])
        self.assertEqual(url, "/tracking/event/update/9999/")
        url = reverse("tracking:event_detail", args=[9999])
        self.assertEqual(url, "/tracking/event/detail/9999/")
        url = reverse("tracking:multi_charter_event_add")
        self.assertEqual(url, "/tracking/mc-event/new/")

    def test_ajax_url_reverse(self):
        url = reverse("tracking:ajax_charter_events", args=[9999])
        self.assertEqual(url, "/tracking/ajax/charter_events/9999/")
        url = reverse("tracking:ajax_ds_charter_list")
        self.assertEqual(url, "/tracking/ajax/charters/")
        url = reverse("tracking:new_charter_modal")
        self.assertEqual(url, "/tracking/ajax/charter/modal/")

    def test_autocomplete_url_reverse(self):
        url = reverse("tracking:charters_autocomplete")
        self.assertEqual(url, "/tracking/ac/charters")
        url = reverse("tracking:charters_autocomplete_lid")
        self.assertEqual(url, "/tracking/ac/charters/lid")

    def test_success_url_reverse(self):
        url = reverse("tracking:charter_add_success", kwargs={"obj_type": "charter", "pk": "9999"})
        self.assertEqual(url, "/tracking/success/charter/9999/")
        url = reverse("tracking:multi_charter_success")
        self.assertEqual(url, "/tracking/success/mc-event/")

    def test_other_url_reverse(self):
        url = reverse("tracking:new_item")
        self.assertEqual(url, "/tracking/new_item/")
