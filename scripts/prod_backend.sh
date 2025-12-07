#!/bin/sh

cd ../backend
gunicorn --bind localhost:9102 --workers 4 main:app