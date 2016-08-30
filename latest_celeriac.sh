#!/usr/bin/env bash

[ -d celeriac ] || git clone https://github.com/fridex/celeriac

(
    cd celeriac
    git pull
    git rev-parse HEAD > ../version_celeriac.txt
    echo "Celeriac commit is now:"
    git --no-pager log -1
)

