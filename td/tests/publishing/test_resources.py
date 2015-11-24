from django.test import TestCase
import requests_mock

from td.publishing.resources import OpenBibleStory, TranslationAcademy


class OpenBibleStoryTestCase(TestCase):

    def setUp(self):
        self.resource = OpenBibleStory("en")

    @requests_mock.mock()
    def test_fetch_chapter(self, mock_requests):
        expected = {
            "number": "01",
            "title": u"1. The Creation",
            "ref": u"A Bible story from: Genesis 1-2",
            "frames": [
                {
                    "id": u"01-01",
                    "img": u"https://example.com/obs/jpg/1/en/360px/obs-en-01-01.jpg",
                    "text": u"This is how the beginning of everything happened.",
                }
            ],
        }
        content = (
            "====== 1. The Creation ======\n\n{{"
            "https://example.com/obs/jpg/1/en/360px/obs-en-01-01.jpg"
            "}}\n\nThis is how the beginning of everything happened."
            "\n\n//A Bible story from: Genesis 1-2//"
        )
        mock_requests.get(
            "https://door43.org/en/obs/01?do=export_raw",
            text=content
        )
        chapter = self.resource.fetch_chapter("01")
        self.assertEquals(chapter, expected)


class TranslationAcademyTestCase(TestCase):

    def setUp(self):
        self.resource = TranslationAcademy("en")

    @requests_mock.mock()
    def test_fetch_chapters(self, mock_requests):
        contents = (
            '<h2 id="volume-1-table-of-contents">Volume 1 Table of Contents</h2>'
            '<div id="plugin_include__en__ta__vol1__intro__toc_intro">'
            '<h3 class="sectionedit4" id="table-of-contents-introduction">'
            'Table of Contents - Introduction</h3><div class="level3">'
            '<p>This module answers the question: What is in the Introduction?<br>'
            '</p></div><h4 id="introduction">Introduction</h4><div class="level4">'
            '<ol><li class="level1"><div class="li"> <a href="/en/ta/vol1/intro/ta_'
            'intro" class="wikilink1" title="en:ta:vol1:intro:ta_intro">Introduction'
            ' to translationAcademy</a></div></li></ol></div></div>'
        )
        expected = {
            'chapters': [
                {
                    'frames': [{
                        'id': u'introduction-to-translationacademy',
                        'ref': u'/en/ta/vol1/intro/ta_intro',
                        'title': u'Introduction to translationAcademy',
                        'text': (
                            u'<h2 id="introduction-to-translationacademy">\n '
                            u'Introduction to translationAcademy\n</h2>'
                        )
                    }],
                    'title': u'Introduction'
                }
            ],
            'id': u'volume-1-table-of-contents',
            'title': u'Volume 1 Table of Contents'
        }
        mock_requests.get(
            "https://door43.org/en/ta/vol1/toc?do=export_xhtmlbody",
            text=contents
        )
        mock_requests.get(
            "https://door43.org/en/ta/vol1/intro/ta_intro?do=export_xhtmlbody",
            text=(
                '<h2 id="introduction-to-translationacademy">Introduction to '
                'translationAcademy</h2>'
            )
        )
        toc = self.resource.fetch_chapters()
        self.assertEquals(toc, expected)

    @requests_mock.mock()
    def test_fetch_frame(self, mock_requests):
        expected = {
            "text": (
                u'<h3 id="/foo/bar">\n Foobar\n</h3>\n<div>\n <a href'
                u'="/foo/bar">\n  foobar\n </a>\n</div>'
            ),
            "id": u"/foo/bar",
            "ref": "/en/ta/vol1/toc",
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

        chapter = self.resource.fetch_frame("/en/ta/vol1/toc")
        self.assertEquals(chapter, expected)
