#!/usr/bin/env python
# auto-generated using Parsley v0.1.0a1 on unused-4-104.brq.redhat.com at 2016-09-05 05:29:27.264675

from parsley.predicates import alwaysTrue, httpStatus, fieldEqual, fieldExist
from tasks import FactTask
from tasks import SumTask
from tasks import MulTask
from tasks import FallbackTask
from celeriac.storage import SqlStorage
from celeriac.storage import RedisStorage
from celeriac.storage import MongoStorage


task_classes = {
    'FactTask': FactTask,
    'SumTask': SumTask,
    'MulTask': MulTask,
    'FallbackTask': FallbackTask
}

def get_task_instance(task_name, flow_name, parent):
    cls = task_classes.get(task_name)
    if not cls:
        raise ValueError("Unknown task with name '%s'" % flow_name)
    return cls(task_name=task_name, flow_name=flow_name, parent=parent)

################################################################################

task2storage_mapping = {
    'FactTask': 'SqlStorage',
    'SumTask': 'RedisStorage',
    'MulTask': 'MongoStorage'
}

_storage_SqlStorage = SqlStorage(connection_string='postgres://postgres:postgres@postgres:5432/postgres')
_storage_RedisStorage = RedisStorage(db=1, host='redis', port=6379, charset='utf-8')
_storage_MongoStorage = MongoStorage(db_name='database_name', collection_name='collection_name', host='mongo', port=27017)
storage2instance_mapping = {
    'SqlStorage': _storage_SqlStorage,
    'RedisStorage': _storage_RedisStorage,
    'MongoStorage': _storage_MongoStorage
}

################################################################################

def is_flow(name):
    return name in ['mainFlow', 'factorialFlow']

################################################################################

output_schemas = {
}

################################################################################

propagate_finished = {
    'mainFlow': True,
    'factorialFlow': False
}

propagate_node_args = {
    'mainFlow': True,
    'factorialFlow': False
}

propagate_parent = {
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
    'FactTask': 5,
    'SumTask': 5,
    'MulTask': 5,
    'FallbackTask': 5
}

################################################################################

time_limit = {
    'FactTask': None,
    'SumTask': None,
    'MulTask': None,
    'FallbackTask': None
}

################################################################################

_mainFlow_fail_SumTask_factorialFlow = {'next': {}, 'fallback': ['FallbackTask']}
_mainFlow_fail_SumTask = {'next': {'factorialFlow': _mainFlow_fail_SumTask_factorialFlow}, 'fallback': []}
_mainFlow_fail_factorialFlow = {'next': {'SumTask': _mainFlow_fail_SumTask_factorialFlow}, 'fallback': []}

_mainFlow_failure_starting_nodes = {
    'SumTask': _mainFlow_fail_SumTask,
    'factorialFlow': _mainFlow_fail_factorialFlow
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

def init():
    pass

################################################################################

def _condition_mainFlow_0(db, node_args):
    return httpStatus(status=200, path='/', host='example.com')


def _condition_mainFlow_1(db, node_args):
    return alwaysTrue()


def _condition_factorialFlow_0(db, node_args):
    return alwaysTrue()


def _condition_factorialFlow_1(db, node_args):
    return (
fieldExist(message=db.get('factorialFlow', 'FactTask'), key='num') and 
(not 
fieldEqual(message=db.get('factorialFlow', 'FactTask'), key='num', value=1)))


################################################################################

edge_table = {
    'mainFlow': [{'from': [], 'to': ['factorialFlow', 'SumTask'], 'condition': _condition_mainFlow_0},
                 {'from': ['factorialFlow', 'SumTask'], 'to': ['MulTask'], 'condition': _condition_mainFlow_1}],
    'factorialFlow': [{'from': [], 'to': ['FactTask'], 'condition': _condition_factorialFlow_0},
                      {'from': ['FactTask'], 'to': ['FactTask'], 'condition': _condition_factorialFlow_1}]
}

################################################################################

