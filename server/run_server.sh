#!/usr/bin/env bash

export LC_ALL=C.UTF-8
export LANG=C.UTF-8

FLASK_APP=server.py exec python3 -m flask run --host 0.0.0.0
