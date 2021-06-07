import os
import sys
from dotenv import dotenv_values
env_list = dotenv_values()


PYTHON_VERSION = sys.version_info[0]
if PYTHON_VERSION == 3:
    import urllib.parse
else:
    raise Exception
    # import urlparse

basedir = os.path.abspath(os.path.dirname(__file__))

if os.path.exists('config.env'):
    for line in open('config.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1].replace("\"", "")


class Config:
    def __init__(self):
        pass

    BASE_URL = 'http://127.0.0.1:8000/'
    APP_NAME = os.environ.get('APP_NAME', 'app')
    os.environ["SECRET_KEY"] = env_list.get('SECRET_KEY', 'asdvjopq2309vh91834')
    if os.environ.get('SECRET_KEY'):
        SECRET_KEY = os.environ.get('SECRET_KEY')
    else:
        SECRET_KEY = 'SECRET_KEY_ENV_VAR_NOT_SET'
        print('SECRET KEY ENV VAR NOT SET! SHOULD NOT SEE IN PRODUCTION')

    REDIS_URL = os.getenv('REDISTOGO_URL', 'http://localhost:6379')

    # Parse the REDIS_URL to set RQ config variables
    if PYTHON_VERSION == 3:
        urllib.parse.uses_netloc.append('redis')
        url = urllib.parse.urlparse(REDIS_URL)
    else:
        raise Exception

    RQ_DEFAULT_HOST = url.hostname
    RQ_DEFAULT_PORT = url.port
    RQ_DEFAULT_PASSWORD = url.password
    RQ_DEFAULT_DB = 0

    @staticmethod
    def init_app(app):
        # mongo config
        app.config['MONGODB_SETTINGS'] = {
            'db': 'mnc_database',
        }
        app.config["TESTING"] = False
        app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
        app.debug = True
        app.config["DEBUG_TB_PANELS"] = (
            "flask_debugtoolbar.panels.versions.VersionDebugPanel",
            "flask_debugtoolbar.panels.timer.TimerDebugPanel",
            "flask_debugtoolbar.panels.headers.HeaderDebugPanel",
            "flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel",
            "flask_debugtoolbar.panels.template.TemplateDebugPanel",
            "flask_debugtoolbar.panels.logger.LoggingPanel",
            "flask_mongoengine.panels.MongoDebugPanel",
        )
        app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


class DevelopmentConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True

    @classmethod
    def init_app(cls, app):
        print('THIS APP IS IN DEBUG MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')


class TestingConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL',
    #     'sqlite:///' + os.path.join(basedir, 'data-test.sqlite'))
    WTF_CSRF_ENABLED = False

    @classmethod
    def init_app(cls, app):
        app.config['MONGODB_SETTINGS'] = {
            'db': 'mnc_test',
        }
        print('THIS APP IS IN TESTING MODE.  \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')


class ProductionConfig(Config):
    DEBUG = False
    USE_RELOADER = False
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
    #     'sqlite:///' + os.path.join(basedir, 'data.sqlite'))
    SSL_DISABLE = (os.environ.get('SSL_DISABLE', 'True') == 'True')

    @classmethod
    def init_app(cls, app):
        app.config['MONGODB_SETTINGS'] = {
            'db': 'mnc_database',
        }
        Config.init_app(app)
        assert os.environ.get('SECRET_KEY'), 'SECRET_KEY IS NOT SET!'


class HerokuConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # Handle proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    'heroku': HerokuConfig,
}