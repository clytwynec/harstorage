#!/usr/bin/env bash

python setup.py develop
paster make-config harstorage production.ini
python runapp.py
