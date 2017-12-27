from flask import current_app
import project.main.analytics as analytics
from project.factory import create_celery_app
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

celery = create_celery_app()

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(120.0, process_mails.s(), name='check emails every 120s')


@celery.task
def process_mails():
    current_app.logger.info("In celery task")
    analytics.analyse_new_chats()
