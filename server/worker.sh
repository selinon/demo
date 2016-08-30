#!/usr/bin/env bash

celery worker --app=tasks -l INFO --concurrency=1
