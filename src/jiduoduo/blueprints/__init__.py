from flask import Flask

from jiduoduo.blueprints import main
from jiduoduo.blueprints import testing
from jiduoduo.blueprints import user
from jiduoduo.blueprints import vps


def register_blueprints(app: Flask):
    app.register_blueprint(main.blueprint)
    app.register_blueprint(user.blueprint)
    app.register_blueprint(vps.blueprint)
    app.register_blueprint(testing.blueprint)
