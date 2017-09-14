from flask import Blueprint, render_template

# config
blog_blueprint = Blueprint('blog', __name__)


# routes
@blog_blueprint.route('/')
def index():
    return "Hello Blog"

