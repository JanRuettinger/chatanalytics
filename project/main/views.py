from flask import Blueprint, render_template

# config
main_blueprint = Blueprint('main', __name__)

# routes

@main_blueprint.route('/')
def index():
    return "Hello Main"
