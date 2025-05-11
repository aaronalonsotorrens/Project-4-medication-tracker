from django.apps import AppConfig


class Project4MedicationTrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'medication_tracker'


    def ready(self):
        import medication_tracker.signals

