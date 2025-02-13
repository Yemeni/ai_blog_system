import os
import json
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Correct path to `languages.json`
LANGUAGE_FILE = os.path.join(settings.BASE_DIR, "lang_manager", "languages.json")

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
        return False  # Language already exists

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
