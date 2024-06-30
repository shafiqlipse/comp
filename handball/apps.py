from django.apps import AppConfig


class HandballConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "handball"

    def ready(self):
        import handball.signals
