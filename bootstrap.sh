#!/bin/bash
export FLASK_APP=./src/app/run.py
source ./venv/bin/activate
cd ./src
python -m app.run --no_debug