#!/usr/bin/env python
# auto-generated using Parsley v58e6228

from parsley.predicates import alwaysTrue

# Tasks
from tasks import Task1
from tasks import Task2
from tasks import Task3
from tasks import Task4
from tasks import Task5


task_classes = {
    'Task1': Task1,
    'Task2': Task2,
    'Task3': Task3,
    'Task4': Task4,
    'Task5': Task5
}

def get_task_instance(task_name, flow_name, parent):
    cls = task_classes.get(task_name)
    if not cls:
        raise ValueError("Unknown task with name '%s'" % flow_name)
    return cls(task_name=task_name, flow_name=flow_name, parent=parent)

################################################################################

task2storage_mapping = {

}

storage2instance_mapping = {

}

################################################################################

def is_flow(name):
    return name in ['flow1', 'flow2']

################################################################################

output_schemas = {
}

################################################################################

propagate_finished = {
    'flow1': False,
    'flow2': False
}

propagate_node_args = {
    'flow1': False,
    'flow2': False
}

propagate_parent = {
    'flow1': False,
    'flow2': False
}

################################################################################

max_retry = {
    'Task1': 1,
    'Task2': 1,
    'Task3': 1,
    'Task4': 1,
    'Task5': 1
}

################################################################################

time_limit = {
    'Task1': 3600,
    'Task2': 3600,
    'Task3': 3600,
    'Task4': 3600,
    'Task5': 3600
}

################################################################################

failures = {
}

################################################################################

nowait_nodes = {
    'flow1': [],
    'flow2': []
}

################################################################################

def init():
    pass

################################################################################

def _condition_flow1_0(db):
    return alwaysTrue()


def _condition_flow1_1(db):
    return alwaysTrue()


def _condition_flow2_0(db):
    return alwaysTrue()


def _condition_flow2_1(db):
    return alwaysTrue()


################################################################################

edge_table = {
    'flow1': [{'from': [], 'to': ['Task1'], 'condition': _condition_flow1_0},
              {'from': ['Task1'], 'to': ['Task2', 'flow2'], 'condition': _condition_flow1_1}],
    'flow2': [{'from': [], 'to': ['Task4'], 'condition': _condition_flow2_0},
              {'from': ['Task4'], 'to': ['Task5'], 'condition': _condition_flow2_1}]
}

################################################################################

