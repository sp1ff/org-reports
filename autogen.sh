#!/usr/bin/env bash
set -e
test -d PyOrgMode && rm -rf PyOrgMode
git clone git@github.com:sp1ff/PyOrgMode.git
virtualenv venv
. venv/bin/activate
cd PyOrgMode
git checkout sp1ff-tag-inheritance
python setup.py install
cd ..
python setup.py develop
pip freeze > requirements.txt
