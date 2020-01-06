#!/bin/sh
source venv/bin/activate

flask db upgrade
exec gunicorn -b :5000 app:app