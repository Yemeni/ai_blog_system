import os
import json

# Manually define BASE_DIR to avoid circular imports
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Set the correct path to `languages.json`
LANGUAGE_FILE = os.path.join(BASE_DIR, "lang_manager", "languages.json")

def load_json_settings():
    """Loads the JSON file and returns parsed data."""
    try:
        with open(LANGUAGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise RuntimeError(f"Configuration file '{LANGUAGE_FILE}' not found.")
    except json.JSONDecodeError:
        raise RuntimeError(f"Error parsing '{LANGUAGE_FILE}'. Ensure it's a valid JSON file.")

def save_languages(data):
    """Saves updated language data back to languages.json."""
    with open(LANGUAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def get_languages():
    """Returns LANGUAGES list from languages.json."""
    language_data = load_json_settings()
    return [(lang[0], lang[1]) for lang in language_data.get("languages", [])]

def get_parler_languages():
    """Returns PARLER_LANGUAGES dictionary from languages.json."""
    language_data = load_json_settings()
    return {
        None: tuple(language_data.get("parler_languages", {}).get("global", [])),
        "default": language_data.get("parler_languages", {}).get("default", {})
    }
