#!/usr/bin/env bash
set -ex

SELINON_YAML_FILES_DIR="../worker/myapp/config"

which which
which selinon-cli || {
    echo "selinon-cli not found, please install it using install_selinon.sh script" >&2
    exit 1
}

PYTHONPATH="../worker/" monkeytype run selinon-cli -vvvv execute \
    --nodes-definition "${SELINON_YAML_FILES_DIR}/nodes.yaml" \
    --flow-definitions "${SELINON_YAML_FILES_DIR}/flows/" \
    --selective-task-names hello_task \
    --flow-name flow1 \
    --node-args '{"name": "Richard Feynman"}' \
    --node-args-json
