#!/usr/bin/env bash
set -e
test -d PyOrgMode && rm -rf PyOrgMode
git clone git@github.com:bjonnh/PyOrgMode.git
virtualenv venv
. venv/bin/activate
cd PyOrgMode
python setup.py install
cd ..
deactivate
pex PyOrgMode -vvv --disable-cache -e orgreports.main:cli -o org-reports.pex ./
. venv/bin/activate
python setup.py develop
pip freeze > requirements.txt
