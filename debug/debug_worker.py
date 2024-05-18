from jiduoduo.tasks import flask_celery_ext

if __name__ == '__main__':
    flask_celery_ext.celery.start([
        'worker', '-l', 'debug'
    ])
