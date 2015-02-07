from eventlog.models import log


def wikipedia_content(session):
    response = session.get("http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes")
    if response.status_code != 200:
        log(
            user=None,
            action="SOURCE_WIKIPEDIA_RELOAD_FAILED",
            extra={"status_code": response.status_code, "text": response.content}
        )
        return
    return response.content


def iso_639_3(session):
    response = session.get("http://www-01.sil.org/iso639-3/iso-639-3.tab")
    if response.status_code != 200:
        log(
            user=None,
            action="SOURCE_SIL_ISO_639_3_RELOAD_FAILED",
            extra={"status_code": response.status_code, "text": response.content}
        )
        return
    return response.content


def ethnologue_language_codes(session):
    response = session.get("http://www.ethnologue.com/sites/default/files/LanguageCodes.tab")
    if response.status_code != 200:
        log(
            user=None,
            action="SOURCE_ETHNOLOGUE_LANG_CODE_RELOAD_FAILED",
            extra={"status_code": response.status_code, "text": response.content}
        )
        return
    return response.content


def ethnologue_country_codes(session):
    response = session.get("http://www.ethnologue.com/sites/default/files/CountryCodes.tab")
    if response.status_code != 200:
        log(
            user=None,
            action="SOURCE_ETHNOLOGUE_COUNTRY_CODE_RELOAD_FAILED",
            extra={"status_code": response.status_code, "text": response.content}
        )
        return
    return response.content


def ethnologue_language_index(session):
    response = session.get("http://www.ethnologue.com/sites/default/files/LanguageIndex.tab")
    if response.status_code != 200:
        log(
            user=None,
            action="SOURCE_ETHNOLOGUE_LANG_INDEX_RELOAD_FAILED",
            extra={"status_code": response.status_code, "text": response.content}
        )
        return
    return response.content


def imdb_people(session):
    response = session.get("http://public.imb.org/globalresearch/Documents/GSEC2015-01/2015-01_GSEC_Listing_of_People_Groups.xls")
    # todo: replace the above line with code to deal with changing file names...
    if response.status_code != 200 or response.content is None or len(response.content) == 0:
        log(
            user=None,
            action="SOURCE_IMB_PEOPLE_GROUPS_RELOAD_FAILED",
            extra={"status_code": response.status_code, "text": response.content}
        )
        return
    return response.content
