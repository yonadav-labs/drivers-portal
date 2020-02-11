from django.apps import AppConfig


class ImporterConfig(AppConfig):
    name = 'importer'

    def ready(self):
        # Ensure tasks are imported by celery
        import importer.tasks
