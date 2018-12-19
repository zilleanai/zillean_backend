import os

from flask_unchained import AppBundleConfig, get_boolean_env


class Config(AppBundleConfig):
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'change-me-to-a-secret-key!')
    SESSION_TYPE = "sqlalchemy"

    MAIL_DEFAULT_SENDER = f"noreply@localhost"  # FIXME

    WEBPACK_MANIFEST_PATH = os.path.join('static', 'assets', 'manifest.json')


class DevConfig(Config):
    EXPLAIN_TEMPLATE_LOADING = False
    SQLALCHEMY_ECHO = False

    WEBPACK_ASSETS_HOST = 'http://localhost:3333'


class ProdConfig(Config):
    pass


class StagingConfig(ProdConfig):
    pass


class TestConfig(Config):
    TESTING = True
