#!/bin/bash

cd ~/parser/
pgrep gunicorn_django | xargs kill
exec gunicorn_django --bind localhost:8001 -w 3 --timeout=900 --graceful-timeout=10 &
