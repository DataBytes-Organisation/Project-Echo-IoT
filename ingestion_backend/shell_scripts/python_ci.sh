#!/bin/bash
VIRTUAL_ENV=".venv"
cd ../python/ingestion
[ ! -d "./$VIRTUAL_ENV" ] && python -m venv $VIRTUAL_ENV
source $VIRTUAL_ENV/Scripts/Activate
pip install -r requirements.txt
pip install -r dev_requirements.txt
coverage run -m pytest
coverage report -m
python -m pylint ./src
python -m pylint ./tests
mypy
cd ../../shell_scripts
