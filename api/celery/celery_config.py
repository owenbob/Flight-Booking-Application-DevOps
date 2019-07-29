from celery import Celery

from api.celery import celery_scheduler


def make_celery(app):
    # create context tasks in celery
    celery = Celery(
        app.import_name,
        broker=app.config["BROKER_URL"]
    )
    celery.conf.update(app.config)
    celery.config_from_object(celery_scheduler)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
