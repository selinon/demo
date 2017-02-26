#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ######################################################################
# Copyright (C) 2016-2017  Fridolin Pokorny, fridolin.pokorny@gmail.com
# This file is part of Selinon project.
# ######################################################################

import os
from celery import Celery
from selinon import Config

_BASE_NAME = os.path.join(os.path.dirname(os.path.relpath(__file__)), 'config')


def init(with_result_backend=False):
    """ Init Celery and Selinon

    :param with_result_backend: true if the application should connect to the result backend
    :return: Celery application instance
    """
    conf = {
        'broker_url': os.environ.get('BROKER_URL', 'amqp://broker:5672'),
    }

    if with_result_backend:
        conf['result_backend'] = os.environ.get('RESULT_BACKEND_URL', 'redis://redis:6379/0')

    app = Celery('myapp')
    app.config_from_object(conf)

    flow_definition_files = []
    # Add all config files for flows
    for conf_file in os.listdir(os.path.join(_BASE_NAME, 'flows')):
        if conf_file.endswith('.yaml') and not conf_file.startswith('.'):
            flow_definition_files.append(os.path.join(_BASE_NAME, 'flows', conf_file))

    # Set Selinon configuration
    Config.set_config_yaml(os.path.join(_BASE_NAME, 'nodes.yaml'), flow_definition_files)
    # Prepare Celery
    Config.set_celery_app(app)

    return app
