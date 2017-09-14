from celery import Celery
from Flask import current_app

current_app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(current_app.name, broker=current_app.config['CELERY_BROKER_URL'])
celery.conf.update(current_app.config)


@celery.task
def my_background_task(arg1, arg2):
    # Download new Emails
    # Analyse Chats
    return 1
