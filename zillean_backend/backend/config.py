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
    SSH_FOLDER = os.path.join(PROJECT_ROOT, 'ssh')

    app_dirs = AppDirs('zillean')
    APP_CACHE_FOLDER = app_dirs.user_cache_dir
    APP_DATA_FOLDER = app_dirs.user_data_dir
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024 * 1024
    # SERVER_NAME=os.getenv('FLASK_SERVER_NAME', 'backend:5000')

    ##########################################################################
    # celery                                                                 #
    ##########################################################################
    CELERY_BROKER_URL = 'redis://{host}:{port}/0'.format(
        host=os.getenv('FLASK_REDIS_HOST', '127.0.0.1'),
        port=os.getenv('FLASK_REDIS_PORT', 6379),
    )
    CELERY_RESULT_BACKEND = CELERY_BROKER_URL

    ##########################################################################
    # mail                                                                   #
    ##########################################################################
    MAIL_SERVER = os.environ.get('FLASK_MAIL_HOST', 'localhost')
    MAIL_PORT = int(os.environ.get('FLASK_MAIL_PORT', 25))
    MAIL_USE_TLS = get_boolean_env('FLASK_MAIL_USE_TLS', False)
    MAIL_USE_SSL = get_boolean_env('FLASK_MAIL_USE_SSL', False)
    MAIL_USERNAME = os.environ.get('FLASK_MAIL_USERNAME', None)
    MAIL_PASSWORD = os.environ.get('FLASK_MAIL_PASSWORD', None)
    MAIL_ADMINS = [os.environ.get('FLASK_MAIL_ADMIN', 'admin@localhost')]
    MAIL_DEFAULT_SENDER = (
        os.environ.get('FLASK_MAIL_DEFAULT_SENDER_NAME', 'Zillean'),
        os.environ.get('FLASK_MAIL_DEFAULT_SENDER_EMAIL',
                       f"noreply@{os.environ.get('FLASK_DOMAIN', 'zillean.ai')}")
    )

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
    # security                                                               #
    ##########################################################################
    FLASH_MESSAGES = False
    SECURITY_PASSWORD_SALT = os.environ.get('FLASK_PASSWORD_SALT', 'security-password-salt')
    SECURITY_CONFIRMABLE = True
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_CHANGEABLE = True

    ADMIN_LOGIN_ENDPOINT = 'admin.login'
    ADMIN_LOGOUT_ENDPOINT = 'admin.logout'
    ADMIN_POST_LOGOUT_ENDPOINT = LocalProxy(
        lambda: url_for('frontend.index', _external=True))

    SECURITY_FORGOT_PASSWORD_ENDPOINT = 'frontend.forgot_password'
    SECURITY_API_RESET_PASSWORD_HTTP_GET_REDIRECT = 'frontend.reset_password'
    SECURITY_INVALID_RESET_TOKEN_REDIRECT = LocalProxy(
        lambda: url_for('frontend.forgot_password', _external=True) + '?invalid')
    SECURITY_EXPIRED_RESET_TOKEN_REDIRECT = LocalProxy(
        lambda: url_for('frontend.forgot_password', _external=True) + '?expired')
    SECURITY_POST_CONFIRM_REDIRECT_ENDPOINT = LocalProxy(
        lambda: url_for('frontend.index', _external=True) + '?welcome')
    SECURITY_CONFIRM_ERROR_REDIRECT_ENDPOINT = LocalProxy(
        lambda: url_for('frontend.resend_confirmation_email', _external=True))

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

    WEBPACK_MANIFEST_PATH = os.path.join('static', 'assets', 'manifest.json')

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
