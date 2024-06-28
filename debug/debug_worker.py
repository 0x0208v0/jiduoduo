from celery import Celery

from jiduoduo.tasks import flask_celery_ext

if __name__ == '__main__':
    celery: Celery = flask_celery_ext.celery

    celery.start([
        'worker',
        '-l', 'info',
        '-c', '2',
        # window系统调试运行需要解除 -P solo 的注释，否则可能无法执行任务
        # https://stackoverflow.com/questions/37255548/how-to-run-celery-on-windows
        # '-P', 'solo',
    ])
