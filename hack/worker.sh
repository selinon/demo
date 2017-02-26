#!/usr/bin/env bash
set -ex

SELINON_YAML_FILES_DIR="/usr/lib/python3.5/site-packages/myapp/config"

# If worker is not configured otherwise, it listens on all queues by default
if [ -z "${WORKER_QUEUES}" ]; then
    WORKER_QUEUES=`selinonlib-cli inspect  \
        -n ${SELINON_YAML_FILES_DIR}/nodes.yaml  \
        -f ${SELINON_YAML_FILES_DIR}/flows/*.yaml  \
        --list-task-queues --list-dispatcher-queue | cut -d':' -f2 | sort -u | tr '\n' ','`
    WORKER_QUEUES="${WORKER_QUEUES:0:-1}" # remove trailing ','
fi

echo "Worker ${HOSTNAME} listening on the following queues: ${WORKER_QUEUES}"
exec celery worker --app=myapp.entrypoint -l INFO --concurrency=1 -Q${WORKER_QUEUES}
