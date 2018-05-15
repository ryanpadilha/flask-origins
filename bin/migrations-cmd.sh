#!/usr/bin/env bash

# initial migration ONLY for SQLite database
export FLASK_APP=wsgi.py
flask db init
flask db migrate
flask db upgrade
