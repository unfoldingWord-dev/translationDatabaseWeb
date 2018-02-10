# Steps to get tD Web running on a development machine:

These instructions start by using the Vagrant VM available here: https://github.com/phillip-hopper/Team43VM.

Also, the instructions assume you are using PyCharm or IntelliJ IDEA.


### Ubuntu prerequisites

    sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk libpq-dev


### Install python versions

    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get update
    sudo apt-get install python2.7 python3.5
    sudo apt-get install python-pip
    sudo apt-get install python3-pip
    sudo apt-get install python-dev
    sudo apt-get install python3-dev
    sudo pip install virtualenv
    sudo pip3 install virtualenv
    sudo apt-get install python-dev


### Virtual environment
Create a new virtual environment with PyCharm/IntelliJ in ~/virtual_env/translationDatabase


### Install Django

    cd ~/virtual_env/translationDatabase
    source ./bin/activate
    pip install django
    pip install requests[security]
    deactivate


### Install Node

    curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
    sudo apt-get install nodejs

    sudo apt-get install npm
    sudo npm cache clean -f
    sudo npm install -g n
    sudo n stable


### Install project python dependencies

    cd ~/virtual_env/translationDatabase
    source ./bin/activate
    cd ~/Projects/translationDatabaseWeb
    pip install 'requests[security]'
    pip install -r requirements.txt
    pip install -r requirements-test.txt
    pip install gondor==1.2.6
    deactivate


### Install Eldarion Cloud CLI

If you need more information on installing the cli, look here: http://eldarion-gondor.github.io/docs/how-to/install-cli/

    sudo sh -c 'curl -s https://storage.googleapis.com/ec-cli/ec-v0.2.2-linux-amd64 > /usr/local/bin/ec'
    sudo chmod +x /usr/local/bin/ec
    sudo ec upgrade


### PGSQL settings

    sudo -u postgres psql
    create user team43 createdb createuser password 'password';
    create database td encoding 'UTF8';
    \q

In `/etc/postgresql/9.3/main/pg_hba.conf` change 

    local   all             all                                     peer
    host    all             all             127.0.0.1/32            peer

to 

    local   all             all                                     trust
    host    all             all             127.0.0.1/32            trust


Now, restart the service: `sudo service postgresql restart`.

Run this script to initialize the database with a dump from the production server:

    ec run db --instance=primary -- pg_dump --no-owner --no-acl | ./manage.py dbshell

If you get timeout errors running the above command, this is an alternative that has worked:

    ec run db --instance=primary -- pg_dump --no-owner --no-acl -T imports_* > dump.sql
    ec run db --instance=primary -- pg_dump --no-owner --no-acl -t imports_* > imports.sql
    ./manage.py dbshell < dump.sql
    ./manage.py dbshell < imports.sql


### Install Redis

    sudo add-apt-repository ppa:chris-lea/redis-server
    sudo apt-get update
    sudo apt-get install redis-server
    redis-benchmark -q -n 1000 -c 10 -P 5


### Other things

  * Follow this to set up the PyCharm/IntelliJ terminal: http://stackoverflow.com/questions/22288569/how-do-i-activate-a-virtualenv-inside-pycharms-terminal
  * Run the site like this: python manage.py runserver
  * To run a management script on td or td-demo server, first switch to master or develop branch and do it like this: 
  ```ec run web python manage.py add_publishing_group```
  If there are command line options for the script, do it like this:
  ```ec run web --cli-option -- python manage.py --command-option add_publishing_group```
  * PostgreSQL repository: `deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main`


### Upgrade PostgreSQL 9.3 to 9.5 on Ubuntu 14.04

This was required because the `publishing_publishrequest` contains a `jsonb` field, a new type that was introduced in PostgreSQL 9.4.

First remove the old version.
Source: http://stackoverflow.com/questions/2748607/how-to-thoroughly-purge-and-reinstall-postgresql-on-ubuntu
```
sudo service postgresql stop
apt-get --purge remove postgresql\*
rm -r /etc/postgresql/
rm -r /etc/postgresql-common/
rm -r /var/lib/postgresql/
userdel -r postgres
groupdel postgres
```

Now add the PostgreSQL repository and install the new version.
Source: http://tecadmin.net/install-postgresql-server-on-ubuntu/
```
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | sudo apt-key add -
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```
