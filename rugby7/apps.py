from django.apps import AppConfig


class Rugby7Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rugby7"

    def ready(self):
        import rugby7.signals
