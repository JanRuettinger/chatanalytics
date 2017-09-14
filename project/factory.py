from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()

def create_app(config_name=None):
    # create app and load config
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('flask.cfg')

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
