#!/usr/bin/env python3
# auto-generated using Selinonlib v0.1.0rc3 on 1c010ed07619 at 2016-10-05 11:54:07.815240

from selinonlib.predicates import fieldEqual, httpStatus, alwaysTrue, fieldExist
from tasks import FactTask as FactTask
from tasks import SumTask as SumTask
from tasks import MulTask as MulTask
from tasks import FallbackTask as FallbackTask
from selinon.storage.sqlStorage import SqlStorage
from selinon.storage.redisStorage import RedisStorage
from selinon.storage.mongoStorage import MongoStorage

import functools
from selinonlib.strategies import biexponential_increase as _strategy_function


task_classes = {
    'FactTask': FactTask,
    'SumTask': SumTask,
    'MulTask': MulTask,
    'FallbackTask': FallbackTask
}

task_queues = {
    'FactTask': 'celery',
    'SumTask': 'celery',
    'MulTask': 'celery',
    'FallbackTask': 'celery'
}

dispatcher_queue = 'celery'

def get_task_instance(task_name, flow_name, parent, finished):
    cls = task_classes.get(task_name)
    if not cls:
        raise ValueError("Unknown task with name '%s'" % flow_name)
    return cls(task_name=task_name, flow_name=flow_name, parent=parent, finished=finished)

################################################################################

task2storage_mapping = {
    'FactTask': 'SqlStorage',
    'SumTask': 'RedisStorage',
    'MulTask': 'MongoStorage'
}

_storage_SqlStorage = SqlStorage(connection_string='postgres://postgres:postgres@postgres:5432/postgres')
_storage_RedisStorage = RedisStorage(host='redis', port=6379, charset='utf-8', db=1)
_storage_MongoStorage = MongoStorage(host='mongo', port=27017, collection_name='collection_name', db_name='database_name')
storage2instance_mapping = {
    'SqlStorage': _storage_SqlStorage,
    'RedisStorage': _storage_RedisStorage,
    'MongoStorage': _storage_MongoStorage
}

################################################################################

def is_flow(name):
    return name in ['mainFlow', 'factorialFlow']

################################################################################

strategy_function = functools.partial(_strategy_function, max_retry=120, start_retry=2)

################################################################################

output_schemas = {
}

################################################################################

propagate_node_args = {
    'mainFlow': True,
    'factorialFlow': False
}

propagate_finished = {
    'mainFlow': True,
    'factorialFlow': False
}

propagate_parent = {
    'mainFlow': False,
    'factorialFlow': False
}

propagate_compound_finished = {
    'mainFlow': False,
    'factorialFlow': False
}

propagate_compound_parent = {
    'mainFlow': False,
    'factorialFlow': False
}

################################################################################

max_retry = {
    'FactTask': 0,
    'SumTask': 0,
    'MulTask': 0,
    'FallbackTask': 0
}

retry_countdown = {
    'FactTask': 0,
    'SumTask': 0,
    'MulTask': 0,
    'FallbackTask': 0
}

time_limit = {
    'FactTask': None,
    'SumTask': None,
    'MulTask': None,
    'FallbackTask': None
}

storage_readonly = {
    'FactTask': False,
    'SumTask': False,
    'MulTask': False,
    'FallbackTask': False
}

################################################################################

_mainFlow_fail_SumTask_factorialFlow = {'next': {}, 'fallback': ['FallbackTask']}
_mainFlow_fail_SumTask = {'next': {'factorialFlow': _mainFlow_fail_SumTask_factorialFlow}, 'fallback': []}
_mainFlow_fail_factorialFlow = {'next': {'SumTask': _mainFlow_fail_SumTask_factorialFlow}, 'fallback': []}

_mainFlow_failure_starting_nodes = {
    'factorialFlow': _mainFlow_fail_factorialFlow,
    'SumTask': _mainFlow_fail_SumTask
}

failures = {
    'mainFlow': _mainFlow_failure_starting_nodes
}

################################################################################

nowait_nodes = {
    'mainFlow': [],
    'factorialFlow': []
}

################################################################################

def init(config_cls):
    return

################################################################################

def _condition_mainFlow_0(db, node_args):
    return httpStatus(host='example.com', path='/', status=200)


def _condition_mainFlow_1(db, node_args):
    return alwaysTrue()


def _condition_factorialFlow_0(db, node_args):
    return alwaysTrue()


def _condition_factorialFlow_1(db, node_args):
    return (
fieldExist(message=db.get('FactTask'), key='num') and 
(not 
fieldEqual(message=db.get('FactTask'), key='num', value=1)))


################################################################################

edge_table = {
    'mainFlow': [{'from': [], 'to': ['factorialFlow', 'SumTask'], 'condition': _condition_mainFlow_0},
                 {'from': ['factorialFlow', 'SumTask'], 'to': ['MulTask'], 'condition': _condition_mainFlow_1}],
    'factorialFlow': [{'from': [], 'to': ['FactTask'], 'condition': _condition_factorialFlow_0},
                      {'from': ['FactTask'], 'to': ['FactTask'], 'condition': _condition_factorialFlow_1}]
}

################################################################################

