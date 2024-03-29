from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler
from flask_mail import Mail


# Create instances with no argument. Will be
# initialized in the function.
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
mail = Mail()
login.login_view = 'auth.login'  # login function


def create_app(config_class=Config):
    # constructs a Flask application instance
    # and eliminate the global variable.
    # Application factory function.

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.upload import bp as upload_bp
    app.register_blueprint(upload_bp)

    # The app.testing flag is going to be True when running
    # unit tests, due to the TESTING variable being set to
    # True in the configuration.
    if not app.debug and not app.testing:
        # enable the email logger when the
        # application is running without debug
        # also when email server exists in the
        # configuration file. All this logging
        # is skipped during unit tests.
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Microblog Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        # for heroku logs
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)

    return app


from app import models
