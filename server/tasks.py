import argparse
from celery import Celery
from celeriac import CeleriacTask, Dispatcher
from celeriac.config import Config

app = Celery('tasks')
app.config_from_object('celeryconfig')


class Task1(CeleriacTask):
    def execute(self, args):
        return {'foo': 'bar'}


class Task2(CeleriacTask):
    def execute(self, args):
        return {'foo': 'bar'}


class Task3(CeleriacTask):
    def execute(self, args):
        return {'foo': 'bar'}



class Task4(CeleriacTask):
    def execute(self, args):
        return {'foo': 'bar'}


class Task5(CeleriacTask):
    def execute(self, args):
        return {'foo': 'bar'}


class Task6(CeleriacTask):
    def execute(self, args):
        return {'foo': 'bar'}

Config.trace_by_logging()
Config.set_config_py('config/config.py')
Config.set_celery_app(app)

