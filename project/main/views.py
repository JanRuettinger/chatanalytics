from flask import Blueprint, render_template, current_app, request, redirect, flash, url_for
from werkzeug.utils import secure_filename
from ..models import Analysis
import project.main.analytics as analytics
# from project.data_analytics import preprocess_data, total_numbers
#import matplotlib.pyplot as plt

# config
main_blueprint = Blueprint('main', __name__)

UPLOAD_FOLDER = '/Users/Jan/Documents/Programming/Python/chatanalytics'
ALLOWED_EXTENSIONS = set(['txt'])


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# routes


@main_blueprint.route('/')
def index():
    current_app.logger.info("In main route")
    return render_template('main/index.html')

@main_blueprint.route('/result/<link>')
def show_result(link):
    result = Analysis.query.filter_by(link_hash = link).first()
    if result:
        path = "/".join(result.path.split("/")[2:])
        return render_template('main/show_result.html', path=path)
    return render_template('main/no_result.html')

@main_blueprint.route('/about')
def about():
   return render_template('main/about.html')


@main_blueprint.route('/privacy')
def privacy():
    return render_template('main/privacy.html')


@main_blueprint.route('/analysis')
def analysis():
    analytics.analyse_new_chats()
    return render_template('main/about.html')


@main_blueprint.route('/instructions')
def instructions():
    return render_template('main/instructions.html')


#@main_blueprint.route('/test', methods=['GET', 'POST'])
#def upload_file():
#    if request.method == 'POST':
#        # check if the post request has the file part
#        if 'file' not in request.files:
#            flash('No file part')
#            return redirect(request.url)
#        file = request.files['file']
#        # if user does not select file, browser also
#        # submit a empty part without filename
#        if file.filename == '':
#            flash('No selected file')
#            return redirect(request.url)
#        if file and allowed_file(file.filename):
#            filename = secure_filename(file.filename)
#            file.save(os.path.join(UPLOAD_FOLDER, filename))
#            return redirect(request.url)
#    return '''
#    <!doctype html>
#    <title>Upload new File</title>
#    <h1>Upload new File</h1>
#    <form method=post enctype=multipart/form-data>
#      <p><input type=file name=file>
#         <input type=submit value=Upload>
#    </form>'''
