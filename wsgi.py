# production 

from project.factory import create_app
app = create_app()  # development, test or production

#import os
#from app import create_app, db
#from app.models import User, Follow, Role, Permission, Post, Comment
#
#app = create_app(os.getenv('FLASK_CONFIG') or 'default')
#
#@app.shell_context_processor
#def make_shell_context():
#    return dict(app=app, db=db, User=User, Follow=Follow, Role=Role,
#                Permission=Permission, Post=Post, Comment=Comment)

#@app.cli.command()
#@click.option('--coverage/--no-coverage', default=False, help='aaa')
#def test(coverage=False):
#    "Test coverage"
#    # ...
#
#@app.cli.command()
#@click.option('--length', default=25, help='Profile stack length')
#@click.option('--profile-dir', default=None, help='Profile directory')
#def profile(length, profile_dir):
#    """Start the application under the code profiler."""
#    # ...
#
#@app.cli.command()
#def deploy():
#    """Run deployment tasks."""
#    # ...
