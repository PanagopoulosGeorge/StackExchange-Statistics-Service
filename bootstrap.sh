#!/bin/bash
export FLASK_APP=./src/app/run.py
source ./venv/bin/activate
cd ./src
python -m app.run --host 0.0.0.0 --port 5001