from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    #Hàm của Customer_User
    # def ready(self):
    #     import app.signals  # Import file signals.py
