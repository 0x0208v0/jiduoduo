import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def run_testing(testing_id):
    logger.info(f'task run_testing start: testing_id={testing_id}')
    from jiduoduo.app import app
    from jiduoduo.services.testing import run_testing as _run_testing

    try:
        with app.app_context():
            _run_testing(testing_id)

    except Exception as e:
        logger.error(f'{e}')

    logger.info(f'task run_testing done: testing_id={testing_id}')
