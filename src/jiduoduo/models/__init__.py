from flask import Flask

from jiduoduo.models.base import db
from jiduoduo.models.testing import Testing
from jiduoduo.models.testing import TestingState
from jiduoduo.models.testing import TestingType
from jiduoduo.models.user import User
from jiduoduo.models.vps import VPS


def register_models(app: Flask):
    db.init_app(app)
