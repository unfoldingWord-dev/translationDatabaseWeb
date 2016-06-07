from mock import patch, PropertyMock

from django.http import JsonResponse
from django.test import TestCase
from djcelery.tests.req import RequestFactory

from td.models import WARegion
from td.utils import flatten_tuple, two_digit_datetime, DataTableSourceView


def setup_view(view, request=None, *args, **kwargs):
    """
    Mimic as_view() by returning the view instance.
    args and kwargs are the same as you would pass to reverse()
    """
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


class FlattenTupleTestCase(TestCase):

    def test_non_tuple_type(self):
        t = "Hobbits"
        self.assertEqual(flatten_tuple(t), (t, ))
        t = 0
        self.assertEqual(flatten_tuple(t), (t, ))
        t = {}
        self.assertEqual(flatten_tuple(t), (t, ))
        t = []
        self.assertEqual(flatten_tuple(t), (t, ))

    def test_no_length(self):
        self.assertTupleEqual(flatten_tuple(()), ())

    def test_flat_tuple(self):
        self.assertTupleEqual(flatten_tuple((1, 2, 3)), (1, 2, 3))

    def test_nested_tuple(self):
        t = (1, (1, ), 1)
        self.assertTupleEqual(flatten_tuple(t), (1, 1, 1))

    def test_nasty_tuple(self):
        t = (1, (1, (1, (1, 1, 1, ())), (1, 1)), (1, (1, 1)))
        self.assertTupleEqual(flatten_tuple(t), (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1))


class TwoDigitDateTimeTestCase(TestCase):

    def test_no_param(self):
        with self.assertRaises(TypeError):
            two_digit_datetime()

    def test_dict_param(self):
        self.assertEqual(two_digit_datetime({}), "{}")

    def test_list_param(self):
        self.assertEqual(two_digit_datetime([]), "[]")

    def test_tuple_param(self):
        self.assertEqual(two_digit_datetime(()), "()")

    def test_empty_string(self):
        self.assertEqual(two_digit_datetime(""), "0")

    def test_one_digit(self):
        self.assertEqual(two_digit_datetime(1), "01")

    def test_two_digit(self):
        self.assertEqual(two_digit_datetime(12), "12")

    def test_three_digit(self):
        self.assertEqual(two_digit_datetime(123), "23")

    def test_one_string(self):
        self.assertEqual(two_digit_datetime("1"), "01")

    def test_two_string(self):
        self.assertEqual(two_digit_datetime("12"), "12")

    def test_three_string(self):
        self.assertEqual(two_digit_datetime("123"), "23")

    def test_word_string(self):
        self.assertEqual(two_digit_datetime("random"), "om")


class DataTableSourceViewTestCase(TestCase):

    def setUp(self):
        self.request = RequestFactory().get('')
        self.view = setup_view(DataTableSourceView(), self.request)

    @patch("td.utils.DataTableSourceView.data", new_callable=PropertyMock, return_value=None)
    @patch("td.utils.DataTableSourceView.draw", new_callable=PropertyMock, return_value=None)
    @patch("td.utils.DataTableSourceView.all_data")
    @patch("td.utils.DataTableSourceView.filtered_data")
    def test_get(self, mock_filtered_data, mock_all_data, mock_draw, mock_data):
        mock_all_data.configure_mock(**{"count.return_value": 0})
        mock_filtered_data.configure_mock(**{"count.return_value": 0})
        result = self.view.get(self.request)
        self.assertIsInstance(result, JsonResponse)
        content = result.content
        self.assertIn("draw", content)
        self.assertIn("data", content)
        self.assertIn("recordsTotal", content)
        self.assertIn("recordsFiltered", content)

    def test_queryset_empty(self):
        self.view.model = WARegion
        self.assertEqual(len(self.view.queryset), 0)

    def test_queryset(self):
        self.view.model = WARegion
        WARegion.objects.get_or_create(name="Middle Earth", slug="middleearth")
        self.assertEqual(len(self.view.queryset), 1)
        WARegion.objects.get_or_create(name="Middle East", slug="middleeast")
        self.assertEqual(len(self.view.queryset), 2)

    def test_paging_start_record(self):
        self.view.request = RequestFactory().get('', {"start": "1"})
        self.assertEqual(self.view.paging_start_record, 1)

    def test_paging_page_length(self):
        self.view.request = RequestFactory().get('', {"length": "1"})
        self.assertEqual(self.view.paging_page_length, 1)
