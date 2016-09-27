#!/usr/bin/env bash

cd /vagrant
virtualenv -p /usr/bin/python3 .env
. .env/bin/activate

python image_search/manage.py runserver
