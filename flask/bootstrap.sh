#!/bin/sh
export FLASK_APP=./userhours-api/index.py

source $(pipenv --venv)/bin/activate

flask run --host 0.0.0.0 --port 8000
