#!/bin/bash

#celery worker --help

celery -A tasks worker --loglevel=info --no-color
