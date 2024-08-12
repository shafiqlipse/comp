from django.apps import AppConfig


class Rugby7sConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rugby7s"

    def ready(self):
        import rugby7s.signals
