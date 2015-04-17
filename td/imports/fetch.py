from eventlog.models import log


class Fetcher(object):

    url = None

    def __init__(self, session):
        self.session = session

    def fetch(self):
        response = self.session.get(self.url)
        if response.status_code != 200:
            log(
                user=None,
                action=self.error_action_label,
                extra={"status_code": response.status_code, "text": response.content}
            )
        return response.content


class WikipediaFetcher(Fetcher):

    url = "http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes"
    error_action_label = "SOURCE_WIKIPEDIA_RELOAD_FAILED"


class WikipediaCountryFetcher(Fetcher):
    url = "http://en.wikipedia.org/wiki/ISO_3166-1"
    error_action_label = "SOURCE_WIKIPEDIA_COUNTRIES_FAILED"


class ISO_639_3Fetcher(Fetcher):

    url = "http://www-01.sil.org/iso639-3/iso-639-3.tab"
    error_action_label = "SOURCE_SIL_ISO_639_3_RELOAD_FAILED"


class EthnologueLanguageCodesFetcher(Fetcher):

    url = "http://www.ethnologue.com/sites/default/files/LanguageCodes.tab"
    error_action_label = "SOURCE_ETHNOLOGUE_LANG_CODE_RELOAD_FAILED"


class EthnologueCountryCodesFetcher(Fetcher):

    url = "http://www.ethnologue.com/sites/default/files/CountryCodes.tab"
    error_action_label = "SOURCE_ETHNOLOGUE_COUNTRY_CODE_RELOAD_FAILED"


class EthnologueLanguageIndexFetcher(Fetcher):

    url = "http://www.ethnologue.com/sites/default/files/LanguageIndex.tab"
    error_action_label = "SOURCE_ETHNOLOGUE_LANG_INDEX_RELOAD_FAILED"


class IMBPeopleFetcher(Fetcher):

    url = "http://public.imb.org/globalresearch/Documents/GSEC2015-01/2015-01_GSEC_Listing_of_People_Groups.xls"
    error_action_label = "SOURCE_IMB_PEOPLE_GROUPS_RELOAD_FAILED"
