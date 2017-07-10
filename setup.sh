#!/usr/bin/env bash

# Parameters
virtualenv_py_dir=soft_environment/python_env
nodeenv_dir=soft_environment/nodejs_env

# Create new environments
virtualenv -p python3.5 $virtualenv_py_dir

# Activate python_env
. $virtualenv_py_dir/bin/activate

# Install requirement packages
pip3 install pip --upgrade
pip3 install setuptools --upgrade
pip3 install wheel --upgrade
pip3 install -r "requirements.txt"

# Frond-end
# Install nodeenv allowing use nodejs inside virtualenv
pip3 install -e git+https://github.com/ekalinin/nodeenv.git#egg=nodeenv

# Create nodejs env
nodeenv $nodeenv_dir

# Activate nodejs_env
. $nodeenv_dir/bin/activate

# Install bower for future front-end installations
npm install -g bower



