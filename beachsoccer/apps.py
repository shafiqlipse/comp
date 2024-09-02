from django.apps import AppConfig


class BeachsoccerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "beachsoccer"

    def ready(self):
        import beachsoccer.signals
