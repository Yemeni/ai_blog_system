from django.core.management.base import BaseCommand
from django.conf import settings
from lang_manager.utils import get_languages, get_parler_languages

class Command(BaseCommand):
    help = "Reloads the LANGUAGES and PARLER_LANGUAGES settings from languages.json"

    def handle(self, *args, **kwargs):
        try:
            # Reload settings dynamically
            settings.LANGUAGES = get_languages()
            settings.PARLER_LANGUAGES = get_parler_languages()

            self.stdout.write(self.style.SUCCESS("Successfully reloaded settings.py! 🚀"))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error reloading settings: {e}"))
