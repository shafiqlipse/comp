from django.apps import AppConfig


class VolleyballConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "volleyball"

    def ready(self):
        import volleyball.signals
