from django.test import TestCase

from td.utils import flatten_tuple, two_digit_datetime


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
