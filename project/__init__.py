from flask import Flask

# config
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('flask.cfg')


# blueprints
from project.blog.views import blog_blueprint
from project.main.views import main_blueprint

app.register_blueprint(main_blueprint)
app.register_blueprint(blog_blueprint, url_prefix='/blog')

