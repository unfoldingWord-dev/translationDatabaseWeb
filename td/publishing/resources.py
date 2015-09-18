import re

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


RESOURCE_TYPES = {
    "obs": OpenBibleStory
}
