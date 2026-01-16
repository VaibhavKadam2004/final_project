from django.apps import AppConfig

class JobsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jobs'    
    def ready(self):
        """
        Import signals when app starts so they're registered with Django.
        This makes all the automatic handlers work.
        """
        import jobs.signals