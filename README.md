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
* `python manage.py loaddata sites`
* `python manage.py loaddata uw_network_seed`
* `python manage.py loaddata uw_region_seed`
* `python manage.py loaddata uw_title_seed`
* `python manage.py loaddata uw_media_seed`
* `python manage.py loaddata additional-languages`
* `python manage.py reload_imports`

At this point, the basic country and language datasets will be populated but without many optional fields or extra data.

### Updating the `/exports/langnames.json` and `/exports/langnames_short.json` endpoints

When languages are added or updated, run this command to update the data locally:

```bash
python manage.py rebuild_langnames
```

Switch to the master branch and run this command to update the data on the server:

```bash
ec run web python manage.py rebuild_langnames
```
## Docker Deployments

translationDatabase was previously built using the [Heroku-18 stack](https://devcenter.heroku.com/articles/heroku-18-stack) and deployed on Heroku dynos.

It is now being deployed using Heroku's Docker container support.

This was configured via:

```
heroku stack:set container -a ${HEROKU_APP_NAME:-translation-database-demo}
```
(and repeated using `HEROKU_APP_NAME=translation-database`).

### Deploying via heroku.yml
This application can be deployed to Heroku via Git.

Heroku's documentation on Git / GitHub deployments can be found here:
- https://devcenter.heroku.com/articles/git
- https://devcenter.heroku.com/articles/github-integration

To deploy the `master` branch to the `translation-database-demo` site:

```
git checkout master
heroku git:remote -a translation-database-demo
git push heroku master:main
```


For additional documentation, see [Building Docker Images with heroku.yml](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml)

### Building the Docker image manually

These instructions are provided as a convenience; the application should be deployable following [Deploying via heroku.yml](#deploying-via-herokuyml) above.

_NOTE_: This assumes that you have a version of [Docker](https://www.docker.com/products/docker-desktop/) installed.

1) Build the production image
```shell
rm -Rf archive archive.tgz
git archive HEAD > archive.tgz
mkdir -p archive
tar -xvf archive.tgz -C archive
cd archive

docker build --platform=linux/amd64 -f Dockerfile -t td .
cd ..
rm -Rf archive
```
2) Run via
```
# assumes environment variables populated in
# .dev-env file
docker run --name=td --rm -d --env-file ./.dev-env -p 8000:8000 td
```
### Push the Docker image to Heroku manually

If you wanted to deploy the pre-built image to Heroku, you would need to:
- have [access](https://devcenter.heroku.com/articles/collaborating) to the `translation-database-demo` and `translation-database` apps on Heroku
- have authenticated with the [Heroku Container Registry](https://devcenter.heroku.com/articles/container-registry-and-runtime#logging-in-to-the-registry)

1) Tag and push for $APP_NAME:
```shell
docker tag td registry.heroku.com/${HEROKU_APP_NAME:-translation-database-demo}/web
docker tag td registry.heroku.com/${HEROKU_APP_NAME:-translation-database-demo}/worker
docker push registry.heroku.com/${HEROKU_APP_NAME:-translation-database-demo}/web
docker push registry.heroku.com/${HEROKU_APP_NAME:-translation-database-demo}/worker
```

3) Release to Heroku
```shell
heroku container:release web worker -a ${HEROKU_APP_NAME:-translation-database-demo}
```

Repeat the steps above with the `HEROKU_APP_NAME` variable set for the production environment:
```shell
export HEROKU_APP_NAME=translation-database
```
