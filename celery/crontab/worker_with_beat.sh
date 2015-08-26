#!/bin/bash

celery -A tasks worker --loglevel=info --no-color --beat
