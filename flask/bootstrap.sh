#!/bin/sh
export FLASK_APP=./userhours-api/index.py

flask run --host 0.0.0.0 --port 8000
