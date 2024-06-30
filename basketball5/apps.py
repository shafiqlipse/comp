from django.apps import AppConfig


class Basketball5Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "basketball5"

    def ready(self):
        import basketball5.signals
