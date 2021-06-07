import os
import werkzeug
from flask import Flask
from config import config as Config
from flask_login import LoginManager
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from dotenv import dotenv_values

import redis
from rq import Queue
from rq.job import Job
from worker import conn
import time

# Set up Flask-Login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'account.login'

db = MongoEngine()

q = Queue(connection=conn)
from app.models import *
from celery import Celery

env_list = dotenv_values()

celery = None


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=env_list['CELERY_RESULT_BACKEND'],
        broker=env_list['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

def create_app(config):
    app = Flask(__name__)

    global celery
    celery = make_celery(app)


    config_key = config
    # Setup the Flask-JWT-Extended extension
    app.config["JWT_SECRET_KEY"] = env_list['JWT_SECRET_KEY']
    jwt = JWTManager(app)

    if not isinstance(config_key, str):
        config_key = os.getenv('FLASK_CONFIG', 'default')

    app.config.from_object(Config[config_key])
    Config[config_key].init_app(app)

    # Setup
    db.init_app(app)
    login_manager.init_app(app)

    # Create app blueprints
    from .root import root as root_blueprint
    from .account import account as account_blueprint
    from .auth import auth as auth_blueprint
    from .report import report as report_blueprint
    from .transaction import transaction as transaction_blueprint
    app.register_blueprint(root_blueprint)
    app.register_blueprint(account_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(report_blueprint)
    app.register_blueprint(transaction_blueprint)

    @app.errorhandler(werkzeug.exceptions.BadRequest)
    def handle_bad_request(e):
        return 'bad request!', 400
    app.register_error_handler(400, handle_bad_request)

    return app

if __name__ == '__main__':
    create_app('default')

