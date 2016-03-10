import requests_mock
import time

from django.contrib.auth.models import User
from django.test import TestCase

from td.models import Language
from td.publishing.models import PublishRequest, OfficialResourceType
from td.publishing.resources import OpenBibleStory, TranslationAcademy


class OpenBibleStoryTestCase(TestCase):
    def setUp(self):
        resource_type, _ = OfficialResourceType.objects.get_or_create(
            short_name="obs",
            long_name="OpenBibleStory"
        )
        language, _ = Language.objects.get_or_create(
            code="en",
            name="English",
            anglicized_name=u'English'
        )
        source_language, _ = Language.objects.get_or_create(
            code="arc",
            name="Aramaic",
            anglicized_name=u'Aramaic'
        )
        self.user, _ = User.objects.get_or_create(
            first_name="Test",
            last_name="RequestorUser",
            username="test_requestor_user"
        )
        self.publish_request, _ = PublishRequest.objects.get_or_create(
            requestor="Test publish request",
            resource_type=resource_type,
            language=language,
            checking_level=1,
            source_text=source_language
        )

        self.resource = OpenBibleStory("en", self.publish_request)

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
        resource_type, _ = OfficialResourceType.objects.get_or_create(
            short_name="ta",
            long_name="translationAcademy"
        )
        language, _ = Language.objects.get_or_create(
            code="en",
            name="English"
        )
        source_language, _ = Language.objects.get_or_create(
            code="arc",
            name="Aramaic"
        )
        self.user, _ = User.objects.get_or_create(
            first_name="Test",
            last_name="RequestorUser",
            username="test_requestor_user"
        )
        self.publish_request, _ = PublishRequest.objects.get_or_create(
            requestor="Test tA publish request",
            resource_type=resource_type,
            language=language,
            checking_level=1,
            source_text=source_language
        )
        self.resource = TranslationAcademy("en", self.publish_request)

    @requests_mock.mock()
    def test_fetch_table_of_contents(self, mock_requests):

        # so unit tests will show the the whole diff if actual does not equal expected
        self.maxDiff = None

        toc = u'## Volume 1 Table of Contents\n\n### Table of Contents - Introduction\n\n'
        toc += u'This module answers the question: What is in the Introduction?  \n\n#### Introduction\n\n'
        toc += u'  1. [Introduction to translationAcademy](/en/ta/vol1/intro/ta_intro "en:ta:vol1:intro:ta_intro" )\n\n'
        expected = {
            'toc': toc,
            'meta': {
                'status': {
                    'source_text': 'arc',
                    'version': '',
                    'publish_date': time.strftime("%Y-%m-%d"),
                    'license': 'CC BY-SA 4.0',
                    'contributors': u'',
                    'checking_level': 1,
                    'checking_entity': '',
                    'source_text_version': u''
                },
                'direction': 'ltr',
                'lc': 'en',
                'anglicized_name': u'',
                'mod': 1457440696,
                'name': 'English'},
            'chapters': [
                {
                    'frames': [
                        {
                            'id': u'vol1_intro_ta_intro',
                            'ref': u'/en/ta/vol1/intro/ta_intro',
                            'title': u'Introduction to translationAcademy',
                            'text': u'<h3>Introduction to translationAcademy</h3>'
                        }
                    ],
                    'title': u'Introduction'
                }
            ]
        }
        contents = (
            '<h2 id="volume-1-table-of-contents">Volume 1 Table of Contents</h2>'
            '<div id="plugin_include__en__ta__vol1__intro__toc_intro" class="plugin_include_content">'
            '<h3 class="sectionedit4" id="table-of-contents-introduction">'
            'Table of Contents - Introduction</h3><div class="level3">'
            '<p>This module answers the question: What is in the Introduction?<br>'
            '</p></div><h4 id="introduction">Introduction</h4><div class="level4">'
            '<ol><li class="level1"><div class="li"> <a href="/en/ta/vol1/intro/ta_'
            'intro" class="wikilink1" title="en:ta:vol1:intro:ta_intro">Introduction'
            ' to translationAcademy</a></div></li></ol></div></div>'
        )
        mock_requests.get(
            "https://door43.org/en/ta/toc?do=export_xhtmlbody",
            text=contents
        )
        mock_requests.get(
            "https://door43.org/en/ta/vol1/intro/ta_intro?do=export_xhtmlbody",
            text=u'<h3>Introduction to translationAcademy</h3>'
        )
        actual = self.resource.fetch_chapters()

        # synchronize the timestamps so they are the same for the test
        expected['meta']['mod'] = actual['meta']['mod']

        self.assertEquals(actual, expected)

    @requests_mock.mock()
    def test_fetch_frame(self, mock_requests):
        expected = {
            "text": (
                u'<h3>Foobar</h3><div><a href'
                u'="/foo/bar">foobar</a></div>'
            ),
            "id": u"vol1_toc",
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
