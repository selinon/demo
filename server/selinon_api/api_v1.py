#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ######################################################################
# Copyright (C) 2016-2017  Fridolin Pokorny, fridolin.pokorny@gmail.com
# This file is part of Selinon project.
# ######################################################################

import logging
from .connection import Connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def post_run_flow(flow_name, node_args=None):
    """ Handler called on POST on /api/v1/run-flow

    :param flow_name: name of flow to be run
    :param node_args: arguments supplied to flow
    :return: resulting dict for the request
    """
    logger.info("Scheduling flow '%s' with node_args: '%s'", flow_name, node_args)
    dispatcher = Connection.run_selinon_flow(flow_name, node_args)
    return {"dispatcher_id": dispatcher.id, "flow_name": flow_name}, 201
