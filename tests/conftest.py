import os
import tempfile

import pytest
import subprocess
from flask import Flask
from flask.cli import run_command
import click
from dotenv import dotenv_values
from app import create_app

from flask_jwt_extended import create_access_token
from app.models.user import Users
from flask.testing import FlaskClient

# from app import create_app, db
# from flaskr.db import get_db
# from flaskr.db import init_db

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    # create the app with common test config
    app = create_app('testing')

    # # create the database and load test data
    # with app.app_context():
    #     init_db()
    #     get_db().executescript(_data_sql)

    yield app

    # # close and remove the temporary database
    # os.close(db_fd)
    # os.unlink(db_path)


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture
def base_url(app):
    return app.config['BASE_URL']
