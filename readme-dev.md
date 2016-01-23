# Steps to get tD Web running on a development machine:

These instructions start by using the Vagrant VM available here: https://github.com/phillip-hopper/Team43VM.

Also, the instructions assume you are using PyCharm or IntelliJ IDEA.


### Ubuntu prerequisites

    sudo apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk


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


### Install Gondor CLI

    sudo curl -s https://storage.googleapis.com/gondor-cli/g3a-v0.7.1-linux-amd64 > /usr/local/bin/g3a 
    sudo chmod +x /usr/local/bin/g3a
    sudo g3a upgrade


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

    g3a run db --instance=primary -- pg_dump --no-owner --no-acl | ./manage.py dbshell

If you get timeout errors running the above command, this is an alternative that has worked:

    g3a run db --instance=primary -- pg_dump --no-owner --no-acl -T imports_* > dump.sql
    g3a run db --instance=primary -- pg_dump --no-owner --no-acl -t imports_* > imports.sql
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
  