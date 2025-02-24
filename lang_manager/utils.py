import os
import json
import subprocess
import sys

# Define BASE_DIR
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGUAGE_FILE = os.path.join(BASE_DIR, "lang_manager", "languages.json")
LOCALE_DIR = os.path.join(BASE_DIR, "AI_Blog_System", "locale") 



def load_languages():
    """Loads languages from languages.json."""
    try:
        with open(LANGUAGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"languages": [], "parler_languages": {"global": [], "default": {}}}

def save_languages(data):
    """Saves updated language data back to languages.json."""
    with open(LANGUAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def get_languages():
    """Returns LANGUAGES list from languages.json."""
    language_data = load_languages()
    return [(lang[0], _(lang[1])) for lang in language_data.get("languages", [])]

def get_parler_languages():
    """Returns PARLER_LANGUAGES dictionary from languages.json."""
    language_data = load_languages()
    return {
        None: tuple(language_data.get("parler_languages", {}).get("global", [])),
        "default": language_data.get("parler_languages", {}).get("default", {})
    }

def add_language(code, name):
    """Adds a new language to languages.json."""
    language_data = load_languages()

    if any(lang[0] == code for lang in language_data["languages"]):
        return False  # Language exists

    language_data["languages"].append([code, name])
    language_data["parler_languages"]["global"].append({"code": code})

    save_languages(language_data)
    return True

def remove_language(code):
    """Removes a language from languages.json."""
    language_data = load_languages()

    language_data["languages"] = [lang for lang in language_data["languages"] if lang[0] != code]
    language_data["parler_languages"]["global"] = [lang for lang in language_data["parler_languages"]["global"] if lang["code"] != code]

    save_languages(language_data)
    return True  # Ensure return value

def generate_translation_files(lang_code):
    """Generates .po and .mo files for a specific language using the correct Python interpreter."""
    locale_path = os.path.join(LOCALE_DIR, lang_code, "LC_MESSAGES")

    # Ensure directory structure
    os.makedirs(locale_path, exist_ok=True)

    try:
        # Use Python executable running Django
        python_executable = sys.executable

        # Generate .po
        subprocess.run([python_executable, "manage.py", "makemessages", "-l", lang_code], check=True)

        # Compile .mo
        subprocess.run([python_executable, "manage.py", "compilemessages"], check=True)

        print(f"✅ Successfully generated .po and .mo for: {lang_code}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error generating translations for {lang_code}: {e}")
        return False


def generate_all_translations():
    """Generates .po and .mo files for all languages in languages.json."""
    language_data = load_languages()
    success_list = []
    error_list = []

    for lang in language_data.get("languages", []):
        lang_code = lang[0]
        if generate_translation_files(lang_code):
            success_list.append(lang_code)
        else:
            error_list.append(lang_code)

    return {
        "success": success_list,
        "failed": error_list
    }

# TODO: extract to separate file

from django.conf import settings
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext as _
from rosetta.conf import settings as rosetta_settings

import polib  # Read .po files


def list_rosetta_translations():
    """Lists all translation fields from Rosetta, including untranslated keys."""
    locale_paths = settings.LOCALE_PATHS
    available_languages = settings.LANGUAGES

    translations = []

    for lang_code, lang_name in available_languages:
        translation_entries = []
        missing_entries = []

        for path in locale_paths:
            po_file_path = os.path.join(path, lang_code, "LC_MESSAGES", "django.po")

            if os.path.exists(po_file_path):
                po = polib.pofile(po_file_path)

                for entry in po:
                    if entry.msgstr.strip():  # If translated
                        translation_entries.append({
                            "original": entry.msgid,
                            "translated": entry.msgstr
                        })
                    else:  # If missing translation
                        missing_entries.append({
                            "original": entry.msgid,
                            "translated": None  # No translation
                        })

                break  # Stop after first valid file

        translations.append({
            "language_code": lang_code,
            "language_name": lang_name,
            "translations": translation_entries if translation_entries else "No translations available",
            "missing_translations": missing_entries if missing_entries else "All translations available"
        })

    return translations



def list_parler_translations():
    """Lists all translations stored by Parler with object IDs."""
    translations = []
    
    for model in TranslatableModel.__subclasses__():  # All translatable models
        for obj in model.objects.all():  # Iterate objects
            for lang_code in obj.get_available_languages():  # Available translations
                obj.set_current_language(lang_code)  # Switch to correct language
                
                translated_fields = {
                    field: getattr(obj, field) for field in model._parler_meta.get_translated_fields()
                }

                translations.append({
                    "model": model.__name__,
                    "object_id": obj.id,  # Include object ID
                    "language_code": lang_code,
                    "translated_fields": translated_fields if translated_fields else "No translations available"
                })

    return translations



def update_rosetta_translation(lang_code, original_text, new_translation):
    """Updates a translation in Rosetta's .po file."""
    locale_paths = settings.LOCALE_PATHS

    for path in locale_paths:
        po_file_path = os.path.join(path, lang_code, "LC_MESSAGES", "django.po")
        if os.path.exists(po_file_path):
            po = polib.pofile(po_file_path)

            # Update translation
            for entry in po:
                if entry.msgid == original_text:
                    entry.msgstr = new_translation
                    po.save()  # Save changes

                    # Compile .mo to apply changes
                    mo_file_path = po_file_path.replace(".po", ".mo")
                    subprocess.run(["msgfmt", "-o", mo_file_path, po_file_path], check=True)

                    return True  # Updated

    return False  # Not found



def update_parler_translation(model_name, object_id, lang_code, field, new_translation):
    """Updates or creates a translation in Parler's database."""
    for model in TranslatableModel.__subclasses__():
        if model.__name__ == model_name:
            try:
                obj = model.objects.get(id=object_id)  # Get object by ID
                available_languages = obj.get_available_languages()

                # If translation missing, create
                if lang_code not in available_languages:
                    obj.create_translation(lang_code)  # Create translation entry

                obj.set_current_language(lang_code)  # Switch to requested language

                if hasattr(obj, field):  # Ensure field exists
                    setattr(obj, field, new_translation)  # Update or create translation
                    obj.save()
                    return True  # Updated or created

            except model.DoesNotExist:
                return False  # Object not found
    return False  # Translation or field not found
