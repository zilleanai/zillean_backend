from flask_unchained import (controller, resource, func, include, prefix,
                             get, delete, post, patch, put, rule)

from .views import SiteController
from flask_unchained.bundles.oauth.views import OAuthController
from flask_unchained.bundles.security import SecurityController, UserResource

routes = lambda: [
    controller(SiteController),
    controller('/auth', SecurityController, rules=[
        get('/confirm/<token>', SecurityController.confirm_email),
        get('/reset-password/<token>', SecurityController.reset_password),
    ]),
    include('flask_unchained.bundles.admin.routes'),
    prefix('/auth', [
        controller(OAuthController)
    ]),
    prefix('/api/v1', [
        controller('/auth', SecurityController, rules=[
            get('/check-auth-token', SecurityController.check_auth_token, only_if=True),
            post('/login', SecurityController.login),
            get('/logout', SecurityController.logout),
            post('/send-confirmation-email', SecurityController.send_confirmation_email),
            post('/forgot-password', SecurityController.forgot_password),
            post('/reset-password/<token>', SecurityController.reset_password,
                 endpoint='security_controller.post_reset_password'),
            post('/change-password', SecurityController.change_password),
        ]),
        resource('/users', UserResource),
    ]),
# frontend routes
    get('/', endpoint='frontend.index'),
    get('/login/forgot-password', endpoint='frontend.forgot_password'),
    get('/login/reset-password/<token>', endpoint='frontend.reset_password'),
    get('/sign-up/resend-confirmation-email',
        endpoint='frontend.resend_confirmation_email'),
]
