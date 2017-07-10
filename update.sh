#!/usr/bin/env bash

git pull

# Activate env
. soft_environment/python_env/bin/activate

# Update dependencies
pip3 install pip --upgrade
pip3 install setuptools --upgrade
pip3 install wheel --upgrade
pip3 install -r "requirements.txt"

# Activate local nodejs env
. soft_environment/nodejs_env/bin/activate

# Install bower dependencies
bower install

# Launch command for project properly app work
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py seed_db
python manage.py loaddata categories_data
python manage.py loaddata products_data

# Switch env off
deactivate
