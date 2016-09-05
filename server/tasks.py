import sys
from celery import Celery
from celeriac import CeleriacTask, Dispatcher
from celeriac.config import Config

app = Celery('tasks')
app.config_from_object('celeryconfig')


class FactTask(CeleriacTask):
    def execute(self, args):
        if 'FactTask' in self.parent:
            prev_result = self.parent_task_result('FactTask')
            num = prev_result['num'] - 1
            res = prev_result['value'] * num
        else:
            assert(args['n'] > 1)
            res = args['n']
            num = args['n']
        return {'value': res, 'num': num}


class SumTask(CeleriacTask):
    def execute(self, args):
        res = args['n'] + args['m']
        return {'value': res}


class MulTask(CeleriacTask):
    def execute(self, args):
        fact_result = self.parent_flow_result('factorialFlow', 'FactTask', -1)
        sum_result = self.parent_task_result('SumTask')
        res = sum_result['value'] * fact_result['value']
        return {'value': res}


class FallbackTask(CeleriacTask):
    def execute(self, args):
        print("We are in FallbackTask", file=sys.stderr)


Config.trace_by_logging()
Config.set_config_py('config/config.py')
Config.set_celery_app(app)

