import sys
import os
from celery import Celery
from selinon import SelinonTask, Dispatcher, Config

app = Celery('tasks')
app.config_from_object('celeryconfig')


class FactTask(SelinonTask):
    def run(self, node_args):
        if 'FactTask' in self.parent:
            prev_result = self.parent_task_result('FactTask')
            num = prev_result['num'] - 1
            res = prev_result['value'] * num
        else:
            assert(node_args['n'] > 1)
            res = node_args['n']
            num = node_args['n']
        return {'value': res, 'num': num}


class SumTask(SelinonTask):
    def run(self, node_args):
        res = node_args['n'] + node_args['m']
        return {'value': res}


class MulTask(SelinonTask):
    def run(self, node_args):
        fact_result = self.parent_flow_result('factorialFlow', 'FactTask', -1)
        sum_result = self.parent_task_result('SumTask')
        res = sum_result['value'] * fact_result['value']
        return {'value': res}


class FallbackTask(SelinonTask):
    def run(self, node_args):
        print("We are in FallbackTask", file=sys.stderr)


Config.trace_by_logging()
Config.set_config_py(os.path.join('config', 'config.py'))
Config.set_celery_app(app)

