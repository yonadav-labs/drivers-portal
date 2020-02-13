from django.apps import AppConfig


class BaseConfig(AppConfig):
    name = 'base'

    def ready(self):
        # Ensure tasks are imported by celery
        import base.tasks
