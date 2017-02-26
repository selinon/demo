#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ######################################################################
# Copyright (C) 2016-2017  Fridolin Pokorny, fridolin.pokorny@gmail.com
# This file is part of Selinon project.
# ######################################################################

import os
import connexion
from flask import redirect
from selinon_api import defaults

app = connexion.App(__name__)
app.add_api(defaults.SWAGGER_YAML_PATH)


@app.route('/')
def base_url():
    # Be nice with user access
    return redirect('api/v1/ui')


if __name__ == '__main__':
    app.run(
        port=int(os.environ.get('SERVICE_PORT', defaults.DEFAULT_SERVICE_PORT)),
        server='flask',
        debug=True
    )
