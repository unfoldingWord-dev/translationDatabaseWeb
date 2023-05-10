FROM python:2.7.18-slim-buster as build
RUN useradd -ms /bin/bash app

RUN apt-get update && apt-get install -y \
    libtiff5-dev libjpeg62-turbo-dev libopenjp2-7-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev \
    libharfbuzz-dev libfribidi-dev libxcb1-dev

USER app
RUN pip install pip wheel --upgrade
WORKDIR /home/app
COPY --chown=app:app requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY --chown=app:app . .
RUN python manage.py collectstatic --noinput
CMD devops/dyno.sh
