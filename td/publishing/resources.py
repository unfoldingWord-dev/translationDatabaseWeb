import re

from bs4 import element, BeautifulSoup
import requests

from docutils.utils.smartquotes import smartyPants


HTML_TAG_RE = re.compile(ur"<.*?>", re.UNICODE)
LINK_TAG_RE = re.compile(ur"\[\[.*?\]\]", re.UNICODE)
IMG_TAG_RE = re.compile(ur"{{.*?}}", re.UNICODE)


def clean_text(input_text):
    """
    cleans up text from possible dokuwiki and html tag polution

    :param input_text:
    :return:
    """
    output_text = HTML_TAG_RE.sub(u"", input_text)
    output_text = LINK_TAG_RE.sub(u"", output_text)
    output_text = IMG_TAG_RE.sub(u"", output_text)
    return output_text


# obs-catalog.json - can make this from data we already have
# obs-{lang}.json - _get_chapters() + app_words (not implemented yet) / stuff data in database
# github file creation (aka uwexport): front_matter, back_matter, qa, langcat
class OpenBibleStory(object):
    img_link_re = re.compile(ur"https://.*\.(jpg|jpeg|gif)", re.UNICODE)
    title_re = re.compile(ur"======.*", re.UNICODE)
    ref_re = re.compile(ur"//.*//", re.UNICODE)
    frame_re = re.compile(ur"{{[^{]*", re.DOTALL | re.UNICODE)
    frid_re = re.compile(ur"[0-5][0-9]-[0-9][0-9]", re.UNICODE)
    num_re = re.compile(ur"([0-5][0-9]).txt", re.UNICODE)
    chapter_numbers = ["{0:02}".format(x) for x in range(1, 51)]
    img_url = "https://api.unfoldingword.org/obs/jpg/1/{0}/360px/obs-{0}-{1}.jpg"
    source_url = "https://door43.org/{lang_code}/obs/{chapter}?do=export_raw"

    def __init__(self, lang_code):
        self.lang_code = lang_code
        self.session = requests.session()

    def _parse(self, regex, raw, replace):
        values = regex.search(raw)
        return values.group(0).replace(replace, "").strip() if values else "NOT FOUND"

    def _parse_img(self, link, frame_id):
        links = self.img_link_re.search(link)
        return links.group(0) if links else self.img_url.format("en", frame_id)

    def _parse_frame_text(self, lines):
        text = u"".join([x for x in lines[1:] if u"//" not in x]).strip()
        text = text.replace(u"\\\\", u"").replace(u"**", u"").replace(u"__", u"")
        text = clean_text(text)
        text = smartyPants(text)
        return text

    def fetch_chapter(self, chapter_number):
        chapter_data = {"frames": [], "number": chapter_number, "ref": "", "title": ""}
        response = self.session.get(
            self.source_url.format(
                lang_code=self.lang_code,
                chapter=chapter_number)
        )
        response.encoding = "utf-8"
        if response.status_code == 200:
            chapter_raw = response.text
            chapter_data["title"] = self._parse(self.title_re, chapter_raw, "=")
            chapter_data["ref"] = self._parse(self.ref_re, chapter_raw, "/")
            for frame in self.frame_re.findall(chapter_raw):
                frame_lines = frame.split("\n")
                frame_ids = self.frid_re.search(frame)
                frame_id = frame_ids.group(0) if frame_ids else "NOT FOUND"
                chapter_data["frames"].append({
                    "id": frame_id,
                    "img": self._parse_img(frame_lines[0], frame_id),
                    "text": self._parse_frame_text(frame_lines[1:])
                })
        return chapter_data

    def fetch_chapters(self):
        return [
            self.fetch_chapter(chapter_number)
            for chapter_number in self.chapter_numbers
        ]


class TranslationAcademy(object):
    """
    Traverse translationAcademy on door43.org, fetching the table of contents
    and then each topic and contents.
    """

    # chapter document IDs in the table of contents
    CHAPTERS = [
        "plugin_include__en__ta__vol1__intro__toc_intro",
        "plugin_include__en__ta__vol1__translate__toc_transvol1",
        "plugin_include__en__ta__vol1__checking__toc_checkvol1",
        "plugin_include__en__ta__vol1__tech__toc_techvol1",
        "plugin_include__en__ta__vol1__process__toc_processvol1",
    ]

    source_url = "https://door43.org{uri}"
    chapters_uri = "/{lang_code}/ta/vol{vol_no}/toc"

    def __init__(self, lang_code, volume_number=1):
        self.lang_code = lang_code
        self.session = requests.session()
        self.session.params = {"do": "export_xhtmlbody"}
        self.volume_number = str(volume_number)

    def _parse_table_of_contents(self, soup):
        """
        Traverse HTML results via BeautifulSoup, returning the table of
        contents

        :param soup: HTML results of the TOC listing via BeautifulSoup
        :type soup: object

        :returns: dict
        """
        page_header_el = soup.find("h2")
        toc = {
            "title": page_header_el.text,
            "id": page_header_el.get("id"),
            "chapters": [],
        }

        # Iterate over each section of the TOC, grabbing the header element's
        # text as the chapter's title, then fetching all links inside the
        # chapter.
        for chapter_id in self.CHAPTERS:
            chapter_el = soup.find(id=chapter_id)
            if chapter_el:
                frames = []
                title = chapter_el.find_next("h3").text
                title = title.replace('Table of Contents - ', '')
                for idx, a_el in enumerate(chapter_el.find_all("a")):
                    frames.append({
                        "number": idx + 1,
                        "name": a_el.text,
                        "url": a_el.get("href"),
                    })
                toc["chapters"].append({"title": title, "frames": frames})
        return toc

    def fetch_frame(self, frame_uri):
        """
        Fetch the content from the `frame_uri`, parsing and formatting the
        input into one expected by the publishing module.

        :param chapter_uri: URI for frame of translationAcademy
        :type chapter_uri: string

        :returns: dict
        """
        frame_url = self.source_url.format(uri=frame_uri)
        response = self.session.get(frame_url)

        if response.ok:
            soup = BeautifulSoup(response.text, "html.parser")
            # Remove HTML comments coming from dokuwiki plugins
            is_html_comment = lambda text: isinstance(text, element.Comment)
            for html_comment in soup.find_all(text=is_html_comment):
                html_comment.extract()

            # Find the page title header
            title_el = soup.find(("h1", "h2", "h3"))
            return {
                "id": title_el.get("id"),
                "ref": frame_uri,
                "title": title_el.text.replace("Table of Contents - ", ""),
                "img": "",
                "text": soup.prettify(formatter="html"),
            }

    def fetch_chapters(self):
        """
        Fetch and return contents of each chapter
        """
        toc = self.fetch_table_of_contents()
        for chapter_no, chapter in enumerate(toc["chapters"]):
            frames = []
            for frame in chapter["frames"]:
                frame_content = self.fetch_frame(frame["url"])
                if not frame_content:
                    frame_content = {
                        "id": frame["name"].lower().replace(" ", "-"),
                        "ref": frame["url"],
                        "title": frame["name"],
                        "img": "",
                        "text": "",
                    }
                frame_content["number"] = frame["number"]
                frames.append(frame_content)

            yield {
                "number": chapter_no,
                "title": chapter["title"],
                "frames": frames,
            }

    def fetch_table_of_contents(self):
        """
        Fetch and parse the table of contents page for translationAcademy

        :returns: dict
        """
        chapters_uri = self.chapters_uri.format(
            lang_code=self.lang_code,
            vol_no=self.volume_number
        )
        chapters_url = self.source_url.format(uri=chapters_uri)
        response = self.session.get(chapters_url)
        if not response.ok:
            response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return self._parse_table_of_contents(soup)


RESOURCE_TYPES = {
    "obs": OpenBibleStory,
    "ta": TranslationAcademy,
}
