import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


def folder_or_none(folder_name):
    if not os.path.exists(os.path.join(PROJECT_ROOT, folder_name)):
        return None
    return folder_name


# these get passed to the FlaskUnchained constructor
TEMPLATE_FOLDER = folder_or_none('templates')
STATIC_FOLDER = folder_or_none('static')
STATIC_URL_PATH = '/static' if STATIC_FOLDER else None
DATA_FOLDER = folder_or_none('data')

BUNDLES = [
    'flask_unchained.bundles.api',
    'flask_unchained.bundles.mail',
    'flask_unchained.bundles.celery',  # move before mail to send emails synchronously
    'flask_unchained.bundles.oauth',
    'flask_unchained.bundles.security',
    'flask_unchained.bundles.session',
    'flask_unchained.bundles.sqlalchemy',
    'flask_unchained.bundles.webpack',

    'backend',  # your app bundle *must* be last
]
