import logging

from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, AnonymousUserMixin
from flask_uuid import FlaskUUID
from flask_marshmallow import Marshmallow
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_migrate import Migrate


class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.name = 'Anonymous'


db = SQLAlchemy()
migrate = Migrate()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = u'Autenticação requerida para acessar a página.'
login_manager.login_message_category = 'info'
login_manager.anonymous_user = Anonymous

flask_uuid = FlaskUUID()
ma = Marshmallow()

f_images = UploadSet('images', IMAGES)


def create_app(mode=None):
    """
        Application Factory for Flask

    :param mode:
    :return:
    """
    if mode:
        instance_path = path.join(
            path.abspath(path.dirname(__file__)), "%s_instance" % mode
        )

        app = Flask('brain',
                    instance_path=instance_path,
                    instance_relative_config=True)

        app.config.from_object('brain.default_settings')
        app.config.from_pyfile('config.py')
    else:
        app = Flask('brain',
                    instance_relative_config=True)

        app.config.from_object('brain.default_settings')

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    flask_uuid.init_app(app)
    ma.init_app(app)

    # logging
    handler = logging.FileHandler(app.config['LOGGING_LOCATION'])
    handler.setLevel(app.config['LOGGING_LEVEL'])
    handler.setFormatter(logging.Formatter(app.config['LOGGING_FORMAT']))
    app.logger.addHandler(handler)

    # flask-uploads
    configure_uploads(app, f_images)

    # blueprint section
    from .views.website import website
    app.register_blueprint(website)

    from .views.auth import auth
    app.register_blueprint(auth)

    from .views.parameter import parameter
    app.register_blueprint(parameter)

    # REST API section
    from .views.website_api import website_api
    app.register_blueprint(website_api)

    return app
