from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # 'apps.accounts' tells Django the full path to this app
    # because it lives inside the apps/ folder, not the root
    name = 'apps.accounts'