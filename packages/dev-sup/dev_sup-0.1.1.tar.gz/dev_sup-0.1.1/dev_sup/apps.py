from django.apps import AppConfig


class DevSupConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dev_sup'

    def ready(self):
        from . import signals
        return super().ready()
