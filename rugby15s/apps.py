from django.apps import AppConfig


class Rugby15sConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rugby15s"

    def ready(self):
        import rugby15s.signals
