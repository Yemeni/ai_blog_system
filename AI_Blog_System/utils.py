import os
import json
import subprocess

# Define BASE_DIR manually
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGUAGE_FILE = os.path.join(BASE_DIR, "lang_manager", "languages.json")
LOCALE_DIR = os.path.join(BASE_DIR, "AI_Blog_System", "locale")  # Set the correct locale directory

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

def reload_settings():
    """Triggers Django management command to reload settings."""
    subprocess.run(["python", "manage.py", "reload_settings"], check=False)

def generate_translation_files(lang_code):
    """Generates .po and .mo files for a new language."""
    locale_path = os.path.join(LOCALE_DIR, lang_code, "LC_MESSAGES")
    
    # Ensure directory structure exists
    os.makedirs(locale_path, exist_ok=True)

    try:
        # Generate .po file
        subprocess.run(["python", "manage.py", "makemessages", "-l", lang_code], check=True)

        # Compile .mo file
        subprocess.run(["python", "manage.py", "compilemessages"], check=True)

        print(f"✅ Successfully generated .po and .mo for: {lang_code}")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error generating translations for {lang_code}: {e}")

import os
import json
import subprocess
from django.conf import settings

# Define BASE_DIR manually
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGUAGE_FILE = os.path.join(BASE_DIR, "lang_manager", "languages.json")
LOCALE_DIR = os.path.join(BASE_DIR, "AI_Blog_System", "locale")  # Set the correct locale directory

def load_json_settings():
    """Loads the JSON file and returns parsed data."""
    try:
        with open(LANGUAGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise RuntimeError(f"Configuration file '{LANGUAGE_FILE}' not found.")
    except json.JSONDecodeError:
        raise RuntimeError(f"Error parsing '{LANGUAGE_FILE}'. Ensure it's a valid JSON file.")

def generate_translation_files(lang_code):
    """Generates .po and .mo files for a specific language."""
    locale_path = os.path.join(LOCALE_DIR, lang_code, "LC_MESSAGES")
    
    # Ensure directory structure exists
    os.makedirs(locale_path, exist_ok=True)

    try:
        # Generate .po file
        subprocess.run(["python", "manage.py", "makemessages", "-l", lang_code], check=True)

        # Compile .mo file
        subprocess.run(["python", "manage.py", "compilemessages"], check=True)

        print(f"✅ Successfully generated .po and .mo for: {lang_code}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error generating translations for {lang_code}: {e}")
        return False


def add_language(code, name):
    """Adds a new language, regenerates translation files, and reloads settings."""
    language_data = load_json_settings()

    if any(lang[0] == code for lang in language_data["languages"]):
        return False  # Language already exists

    language_data["languages"].append([code, name])
    language_data["parler_languages"]["global"].append({"code": code})

    save_languages(language_data)

    # Generate translation files automatically
    generate_translation_files(code)

    # Automatically reload settings
    reload_settings()

    return True

