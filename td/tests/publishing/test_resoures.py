from django.test import TestCase
import requests_mock

from td.publishing.resources import TranslationAcademy


class TranslationAcademyTestCase(TestCase):

    def setUp(self):
        self.resource = TranslationAcademy('en')

    @requests_mock.mock()
    def test_fetch_table_of_contents(self, mock_requests):
        contents = (
            '<h3 id="/foo/bar">Foobar</h3><!--comment--><div>'
            '<a href="/foo/bar">foobar</a></div>'
        )
        mock_requests.get(
            'https://door43.org/en/ta/vol1/toc?do=export_xhtmlbody',
            text=contents
        )

        toc = self.resource.fetch_table_of_contents()
        self.assertEquals(str(toc), contents)

    @requests_mock.mock()
    def test_parse_table_of_contents(self, mock_requests):
        expected = {
            'id': u'/foo/bar',
            'sections': [{
                'pages': [{'name': u'foobar2', 'url': u'/foo/bar/2'}],
                'title': 'Foobar2',
            }],
            'title': u'Foobar'
        }
        contents = (
            '<h2 id="/foo/bar">Foobar</h2><!--comment--><h3 id="/foo/bar/2">'
            'Foobar2</h3><div><a href="/foo/bar/2">foobar2</a></div><a href="/pag'
            'e/footer">PageFooter</a>'
        )
        mock_requests.get(
            'https://door43.org/en/ta/vol1/toc?do=export_xhtmlbody',
            text=contents
        )

        toc_soup = self.resource.fetch_table_of_contents()
        toc = self.resource._parse_table_of_contents(toc_soup)
        self.assertEquals(toc, expected)

    @requests_mock.mock()
    def test_fetch_chapter(self, mock_requests):
        expected = {
            "frames": [{
                "text": (
                    u'<h3 id="/foo/bar">\n Foobar\n</h3>\n<div>\n <a href'
                    u'="/foo/bar">\n  foobar\n </a>\n</div>'
                ),
                "id": u"/foo/bar",
                "img": None
            }],
            "ref": "https://door43.org/en/ta/vol1/toc",
            "number": u"/foo/bar",
            "title": u"Foobar"
        }
        contents = (
            '<h3 id="/foo/bar">Foobar</h3><!--comment--><div><a href="/foo/bar'
            '">foobar</a></div>'
        )
        mock_requests.get(
            "https://door43.org/en/ta/vol1/toc?do=export_xhtmlbody",
            text=contents
        )

        chapter = self.resource.fetch_chapter("/en/ta/vol1/toc")
        self.assertEquals(chapter, expected)
