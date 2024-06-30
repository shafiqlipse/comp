from django.apps import AppConfig


class Basketball3Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "basketball3"

    def ready(self):
        import basketball3.signals
