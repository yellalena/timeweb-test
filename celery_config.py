from celery import Celery


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend='rpc://',
        broker=f'amqp://myuser:mypassword@localhost:5672//'
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

