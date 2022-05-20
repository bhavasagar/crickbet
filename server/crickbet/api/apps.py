import imp
from django.apps import AppConfig
from .schedulers import get_live_matches

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        print('Starting APP...')
        get_live_matches()
        return super().ready()
