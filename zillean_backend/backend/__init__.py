from flask import Flask, session
from flask_unchained import AppBundle, FlaskUnchained


class BackendBundle(AppBundle):
    @classmethod
    def before_init_app(cls, app: Flask):
        app.url_map.strict_slashes = False

    @classmethod
    def after_init_app(cls, app: FlaskUnchained):
        app.jinja_env.add_extension('jinja2_time.TimeExtension')
