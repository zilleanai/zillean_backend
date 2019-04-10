from flask_unchained import (controller, resource, func, include, prefix,
                             get, delete, post, patch, put, rule)

from .views import SiteController
from flask_unchained.bundles.oauth.views import OAuthController

routes = lambda: [
    controller(SiteController),
    prefix('/auth', [
        resource(OAuthController)
    ]),
]
