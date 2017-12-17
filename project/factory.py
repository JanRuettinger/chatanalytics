from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from celery import Celery
import os

db = SQLAlchemy()
mail = Mail()

CELERY_TASK_LIST = [
    'project.main.tasks',
]

def create_app():
    # create app and load config
    app = Flask(__name__, instance_relative_config=True)
    load_config(app)

    db.init_app(app)
    migrate = Migrate(app, db)
    mail.init_app(app)

    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........
        db.create_all()
    # blueprints
    from project.blog.views import blog_blueprint
    from project.main.views import main_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(blog_blueprint, url_prefix='/blog')

    return app


def load_config(app):
    config = os.environ["FLASK_CONFIG"].lower()

    if config == "test":
        # load default_settings
        app.config.from_object('project.default_settings')

        app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
        app.config['MAIL_SERVER'] = os.environ["MAIL_SERVER"]
        app.config['IMAP_SERVER'] = os.environ["IMAP_SERVER"]
        app.config['MAIL_USERNAME'] = os.environ["MAIL_USERNAME"]
        app.config['MAIL_PASSWORD'] = os.environ["MAIL_PASSWORD"]

    if config == "development":
        app.config.from_pyfile('development.cfg')

    if config == "production":
        app.config.from_pyfile('production.cfg')



def create_celery_app(app=None):
    """
    Create a new Celery object and tie together the Celery config to the app's
    config. Wrap all tasks in the context of the application.
    :param app: Flask app
    :return: Celery app
    """
    app = app or create_app()

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'],
                    include=CELERY_TASK_LIST)
    celery.conf.update(app.config)
    celery.conf.update(CELERYD_HIJACK_ROOT_LOGGER=False)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
