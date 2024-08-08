from flask import Flask

from jiduoduo.tasks.base import flask_celery_ext
from jiduoduo.tasks.testing import run_testing


def register_tasks(app: Flask):
    flask_celery_ext.init_app(app)
