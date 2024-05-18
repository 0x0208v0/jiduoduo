from celery import Celery

from jiduoduo.tasks import flask_celery_ext

if __name__ == '__main__':
    celery: Celery = flask_celery_ext.celery

    # https://stackoverflow.com/questions/37255548/how-to-run-celery-on-windows

    celery.start([
        'worker',
        '-l', 'info',
        '-c', '1',
        '-P', 'solo',
    ])
