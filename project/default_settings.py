import os


# grab the folder of the top-level directory of this project
BASEDIR = os.path.abspath(os.path.dirname(__file__))
TOP_LEVEL_DIR = os.path.abspath(os.curdir)
RESULT_URL = 'http://localhost:5000/result/'
OUTPUTDIR = 'project/static/img/' # Results


# Database config
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/chatanalytics'
SQLALCHEMY_TRACK_MODIFICATIONS = False

MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_SENDER = 'Admin <chat@chatanalytics.io>'

# Celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND= 'redis://localhost:6379/0'

# Test config
DEBUG = False
TESTING = True
