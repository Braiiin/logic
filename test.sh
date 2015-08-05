#!/usr/bin/env bash

source env/bin/activate
py.test tests
deactivate