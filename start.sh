#!/bin/bash
python -m venv /opt/venv
source /opt/venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate && python manage.py runserver 0.0.0.0:8000
