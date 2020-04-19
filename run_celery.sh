#!/bin/bash
CMD="celery worker -A movies_app --autoscale=${CELERY_WORKERS_MAX:=20},${CELERY_WORKERS_MIN:=3} -E -l info"
${CMD}
