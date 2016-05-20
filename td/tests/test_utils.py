from django.test import TestCase

from td.utils import flatten_tuple


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
