#!/usr/bin/env bash

[ -d parsley ] || git clone https://github.com/fridex/parsley

(
    cd parsley
    git pull
    git rev-parse HEAD > ../version_parsley.txt
    echo "Parsley commit is now:"
    git --no-pager log -1
)

./parsley/parsley-cli.py -nodes server/config/nodes.yml -flow server/config/flows/* -dump server/config/config.py

