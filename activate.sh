#!/usr/bin/env bash

# check for virtualenv and datastore
[ -d "env" ] && python3 -m venv env

mkdir -p env/db

# activate virtualenv
source env/bin/activate

# run mongodb in background
mongod --dbpath env/db &

# launch server itself
python3 run.py

mongo 127.0.0.1/admin --eval "db.shutdownServer()"

deactivate