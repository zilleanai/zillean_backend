import os
import redis

from appdirs import AppDirs
from datetime import timedelta
from flask_unchained import AppBundleConfig, get_boolean_env, url_for
from werkzeug.local import LocalProxy


class Config(AppBundleConfig):
    ##########################################################################
    # flask                                                                  #
    ##########################################################################
    DEBUG = get_boolean_env('FLASK_DEBUG', False)
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'change-me-to-a-secret-key!')
    APP_ROOT = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_ROOT, os.pardir))
    DATA_FOLDER = os.path.join(PROJECT_ROOT, 'data')

    app_dirs = AppDirs('zillean')
    APP_CACHE_FOLDER = app_dirs.user_cache_dir
    APP_DATA_FOLDER = app_dirs.user_data_dir

    ##########################################################################
    # celery                                                                 #
    ##########################################################################
    CELERY_BROKER_URL = 'redis://{host}:{port}/0'.format(
        host=os.getenv('FLASK_REDIS_HOST', '127.0.0.1'),
        port=os.getenv('FLASK_REDIS_PORT', 6379),
    )
    CELERY_RESULT_BACKEND = CELERY_BROKER_URL

    ##########################################################################
    # session/cookies                                                        #
    ##########################################################################
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.Redis(
        host=os.getenv('FLASK_REDIS_HOST', '127.0.0.1'),
        port=int(os.getenv('FLASK_REDIS_PORT', 6379)),
    )
    SESSION_PROTECTION = 'strong'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True

    # SECURITY_TOKEN_MAX_AGE is fixed from time of token generation;
    # it does not update on refresh like a session timeout would. for that,
    # we set (the ironically named) PERMANENT_SESSION_LIFETIME
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)

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

    ##########################################################################
    # oauth                                                                  #
    ##########################################################################

    OAUTH_REMOTE_APP_GITLAB = dict(
        consumer_key=os.getenv('OAUTH_GITLAB_CONSUMER_KEY', ''),
        consumer_secret=os.getenv('OAUTH_GITLAB_CONSUMER_SECRET', ''),
        base_url='https://gitlab.com/api/v4/user',
        access_token_url='https://gitlab.com/oauth/token',
        access_token_method='POST',
        authorize_url='https://gitlab.com/oauth/authorize',
        request_token_url=None,
        request_token_params={'scope': 'openid read_user'},
    )


class DevConfig(Config):
    EXPLAIN_TEMPLATE_LOADING = False
    SQLALCHEMY_ECHO = False

    # WEBPACK_ASSETS_HOST = 'http://localhost:3333'
    SESSION_COOKIE_SECURE = False

class ProdConfig(Config):
    pass


class StagingConfig(ProdConfig):
    pass


class TestConfig(Config):
    TESTING = True
