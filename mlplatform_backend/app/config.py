import os

from flask_unchained import AppBundleConfig, get_boolean_env


class Config(AppBundleConfig):
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'change-me-to-a-secret-key!')
    SESSION_TYPE = "sqlalchemy"

    ##########################################################################
    # database                                                               #
    ##########################################################################
    SQLALCHEMY_DATABASE_URI = '{engine}://{user}:{pw}@{host}:{port}/{db}'.format(
        engine=os.getenv('FLASK_DATABASE_ENGINE', 'postgresql+psycopg2'),
        user=os.getenv('FLASK_DATABASE_USER', 'flask_api'),
        pw=os.getenv('FLASK_DATABASE_PASSWORD', 'flask_api'),
        host=os.getenv('FLASK_DATABASE_HOST', '127.0.0.1'),
        port=os.getenv('FLASK_DATABASE_PORT', 5432),
        db=os.getenv('FLASK_DATABASE_NAME', 'flask_api'))

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
