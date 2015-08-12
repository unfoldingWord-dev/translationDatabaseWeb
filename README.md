translationDatabase
===================

[![Build Status](https://travis-ci.org/unfoldingWord-dev/translationDatabaseWeb.svg)](https://travis-ci.org/unfoldingWord-dev/translationDatabaseWeb)
[![Coverage Status](https://img.shields.io/coveralls/unfoldingWord-dev/translationDatabaseWeb.svg)](https://coveralls.io/r/unfoldingWord-dev/translationDatabaseWeb)

## Goals

The goals for translationDatabase are to manage and track data for languages and the progress of getting unrestricted biblical content into every language.

For more information on the unfoldingWord project, see the [About page](https://unfoldingword.org/about/).

## Data Sources

A lot of the sources of data are pull into and managed as repo as part of the
Debian project called simply, [ISO Codes](https://alioth.debian.org/anonscm/git/iso-codes/iso-codes.git).

### In Use

* [ISO 639-1 - Wikipedia](http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
* [ISO 639-3 - SIL - Code Set](http://www-01.sil.org/iso639-3/iso-639-3.tab)
* [Ethnologue Data](http://www.ethnologue.com/codes/download-code-tables)

### Other Potential Sources

* [ISO 639-2 - LOC](http://www.loc.gov/standards/iso639-2/)
* [ISO 639-3 - SIL - Names Index](http://www-01.sil.org/iso639-3/iso-639-3_Name_Index.tab)
* [ISO 639-3 - SIL - Macrolanguage Mappings](http://www-01.sil.org/iso639-3/iso-639-3-macrolanguages.tab)
* [ISO 639-3 - SIL - Retirements](http://www-01.sil.org/iso639-3/iso-639-3_Retirements.tab)
* [ISO 3166 - ISO](http://www.iso.org/iso/country_codes)
* [ISO 15924 - Codes for the representation of names of scripts](http://www.unicode.org/iso15924/iso15924.txt.zip)
* [Unicode Supplemental Data](http://unicode.org/repos/cldr/trunk/common/supplemental/supplementalData.xml)
* [Geo Names - Languages in their own writing systems](http://www.geonames.de/languages.html)
* [Glottolog](http://glottolog.org)

## Getting Started

To setup a new working environment of this project, several items are needed:

* Python (consult the requirements.txt for specific libraries/packages)
* Redis
* Postgres
* Node

### Building Static Media

    npm install
    npm run watch     # run a watcher on the static folder
    npm run build     # builds static and exits
    npm run buildprod # builds for production (uglify/minification)


### Initialize the Database

After installing requirements (via pip) within your environment or virtualenv:

* `python manage.py migrate`
* `python manage.py loaddata uw_network_seed`
* `python manage.py loaddata uw_region_seed`
* `python manage.py loaddata uw_title_seed`
* `python manage.py loaddata uw_media_seed`
* `python manage.py loaddata additional-languages`
* `python manage.py reload_imports`

At this point, the basic country and language datasets will be populated but without many optional fields or extra data.
