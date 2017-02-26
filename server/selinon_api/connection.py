#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ######################################################################
# Copyright (C) 2016-2017  Fridolin Pokorny, fridolin.pokorny@gmail.com
# This file is part of Selinon project.
# ######################################################################

from selinon import run_flow
from myapp.configuration import init


class Connection(object):
    """ Connect to broker handling """
    _connected = False

    def __init__(self):
        raise NotImplementedError()

    @classmethod
    def run_selinon_flow(cls, flow_name, node_args):
        """ Run Selinon flow, connect to broker if necessary

        :param flow_name: name of flow to run
        :param node_args: flow arguments
        :return: celery.AsyncResult describing dispatcher task
        """
        if not cls._connected:
            # It is not necessary to connect to result backend, we just publish messages
            init(with_result_backend=False)
            cls._connected = True

        return run_flow(flow_name, node_args)
