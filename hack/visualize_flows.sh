#!/usr/bin/env bash
set -ex

SELINON_YAML_FILES_DIR="../worker/myapp/config"

which which
which selinon-cli || {
    echo "selinon-cli not found, please install it using install_selinon.sh script" >&2
    exit 1
}

selinon-cli plot \
    --nodes-definition "${SELINON_YAML_FILES_DIR}/nodes.yaml" \
    --flow-definitions "${SELINON_YAML_FILES_DIR}/flows/" \
    --output-dir . \
    --format 'svg'

#selinon-cli inspect \
#    --nodes-definition "${SELINON_YAML_FILES_DIR}/nodes.yaml" \
#    --flow-definitions "${SELINON_YAML_FILES_DIR}/flows/" \
#    --dump out.py
