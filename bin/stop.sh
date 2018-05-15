#!/bin/bash
#
# This script stop python application using Gunicorn

echo "stop python application"

PID=$(cat /var/company/run/gunicorn-flask-origins.pid)
kill -9 $PID
