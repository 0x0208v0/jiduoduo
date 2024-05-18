import logging
import os
import pathlib
import secrets
import uuid

from filelock import FileLock
from flask import Flask
from flask_login import LoginManager

from jiduoduo.blueprints import register_blueprints
from jiduoduo.config import config
from jiduoduo.models import User
from jiduoduo.models import db
from jiduoduo.models import register_models
from jiduoduo.tasks import register_tasks

logging.basicConfig(format=config.LOGGING_FORMAT, level=config.LOGGING_LEVEL)
logger = logging.getLogger(__name__)

app = Flask(__name__, instance_path=os.getcwd())
app.config.update(config.model_dump())

login_manager = LoginManager(app)
login_manager.login_view = 'user.login'
login_manager.login_message = '访问该页面需要先登陆'


@login_manager.user_loader
def load_user(user_id: uuid.UUID):
    return User.get(user_id)


register_models(app)
register_blueprints(app)
register_tasks(app)


@login_manager.user_loader
def load_user(user_id: int):
    return db.session.get(User, user_id)


with app.app_context():
    db.create_all()

    env_file_path = pathlib.Path('.env')
    if not env_file_path.exists():
        with FileLock(".env.lock") as lock:
            if not env_file_path.exists():
                with open('.env', 'w+') as f:
                    secret_key = secrets.token_hex(16)
                    f.write(f'SECRET_KEY={secret_key}')
