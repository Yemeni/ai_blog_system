from django.apps import AppConfig
from django.conf import settings
import sys  # Import sys to check command-line arguments

class LangManagerConfig(AppConfig):
    name = 'lang_manager'

    def ready(self):
        # Skip DB queries during migrations
        if 'migrate' not in sys.argv and 'makemigrations' not in sys.argv:
            from .utils import get_active_languages
            settings.PARLER_LANGUAGES = {
                None: get_active_languages(),
                'default': {
                    'fallbacks': ['en'],
                    'hide_untranslated': False,
                }
            }
