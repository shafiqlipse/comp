from django.apps import AppConfig


class HockeyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hockey"

    def ready(self):
        import hockey.signals
