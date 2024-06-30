from django.apps import AppConfig


class NetballConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "netball"

    def ready(self):
        import netball.signals
