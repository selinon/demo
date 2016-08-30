#!/usr/bin/env python
import os
import shutil
from parsley import System
from flask import render_template

from celery import Celery
from celeriac import  Dispatcher
from celeriac.config import Config

FLOWS_TEMPLATE = 'flows.html'
YAML_FILES_DIR = os.path.join(os.getcwd(), 'config')
YAML_FILES_DIR_BAC = os.path.join(os.getcwd(), 'config_bac')
FLOW_GRAPHS_DIR = os.path.join(YAML_FILES_DIR, 'graphs')
CONFIG_PY_PATH = os.path.join(YAML_FILES_DIR, 'config.py')

# Connect to Celery
celery_app = Celery('tasks')
celery_app.config_from_object('celeryconfig')


class ServerFlowInfo(object):
    _system = None
    _config_files = None
    _config_py = None

    def __init__(self):
        raise NotImplementedError()

    @classmethod
    def _update_config_files(cls):
        nodes_yml = os.path.join(YAML_FILES_DIR, 'nodes.yml')

        if not os.path.isfile(nodes_yml):
            nodes_yml = os.path.join(YAML_FILES_DIR, 'nodes.yaml')
            if not os.path.isfile(nodes_yml):
                raise ValueError("nodes.yml not found in config")

        flows_dir = os.path.join(YAML_FILES_DIR, 'flows')

        if not os.path.isdir(flows_dir):
            raise ValueError("Missing directory flows in config")

        flows = []
        for flow in os.listdir(flows_dir):
            if not flow.endswith(".yml") and not flow.endswith(".yaml"):
                raise ValueError("Unknown file found in config: '%s'" % flow)
            flows.append(os.path.join(flows_dir, flow))

        cls._config_files = nodes_yml, flows

        return cls._config_files

    @classmethod
    def _init_system(cls, force=False):
        if cls._system is None or force:
            cls._update_config_files()
            cls._system = System.from_files(cls._config_files[0], cls._config_files[1])
            cls._system.plot_graph(FLOW_GRAPHS_DIR, image_format='png')
            cls._system.dump2file(CONFIG_PY_PATH)

    @classmethod
    def render_flow_template(cls):
        cls._init_system()
        flow_usage = {}
        for flow in cls._system.flows:
            # TODO: add used nodes
            flow_usage[flow.name] = []

        return render_template(FLOWS_TEMPLATE, flow_usage=flow_usage)

    @classmethod
    def get_config_files(cls):
        if cls._config_files is None:
            cls._update_config_files()
        return cls._config_files

    @classmethod
    def from_archive(cls, file_path):
        # we make a backup of the current config, do not run flask with concurrency
        shutil.move(YAML_FILES_DIR, YAML_FILES_DIR_BAC)
        os.mkdir(YAML_FILES_DIR)
        try:
            shutil.unpack_archive(file_path, YAML_FILES_DIR)
            cls._init_system(force=True)
            shutil.rmtree(YAML_FILES_DIR_BAC)
        except:
            shutil.rmtree(YAML_FILES_DIR)
            shutil.move(YAML_FILES_DIR_BAC, YAML_FILES_DIR)
            raise

    @classmethod
    def run(cls, flow_name, args):
        Config.trace_by_logging()
        Config.set_config_py(CONFIG_PY_PATH)
        Config.set_celery_app(celery_app)
        async_result = Dispatcher().delay(flow_name, args)
        return async_result.task_id
