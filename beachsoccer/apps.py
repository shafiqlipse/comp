from django.apps import AppConfig


class BeachSoccerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "beachsoccer"

    def ready(self):
        import beachsoccer.signals
