from django.apps import AppConfig

class AppGestionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_gestion'

    def ready(self):
        import app_gestion.signals