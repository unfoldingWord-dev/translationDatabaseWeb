from django.test import TestCase
from td.gl_tracking.models import Partner
from td.gl_tracking.import_widgets import NullableForeignKeyWidget


class testNullableForeignKeyWidget(TestCase):

    def setUp(self):
        self.record = Partner(name="test partner")
        self.record.save()

    def test_valid_value(self):
        widget = NullableForeignKeyWidget(Partner, "name")
        self.assertEqual(widget.clean("test partner").id, self.record.id)

    def test_invalid_value(self):
        widget = NullableForeignKeyWidget(Partner, "name")
        self.assertEqual(widget.clean("unknown partner"), None)

    def tearDown(self):
        self.record.delete()
