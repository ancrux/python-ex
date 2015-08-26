#!/bin/bash

# --max-interval=10 equals to CELERYBEAT_MAX_LOOP_INTERVAL = 10 in celeryconfig.py
celery -A tasks beat -l info -C --max-interval=10
