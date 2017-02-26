#!/usr/bin/env bash
set -ex

SELINON_YAML_FILES_DIR="../worker/myapp/config"

which which
which selinonlib-cli || {
    echo "selinonlib-cli not found, please install it using install_selinon.sh script" >&2
    exit 1
}

selinonlib-cli plot \
    --nodes-definition "${SELINON_YAML_FILES_DIR}/nodes.yaml" \
    --flow-definitions "${SELINON_YAML_FILES_DIR}/flows/"*.yaml \
    --output-dir . \
    --format 'svg'
