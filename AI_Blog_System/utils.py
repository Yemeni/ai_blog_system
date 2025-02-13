import os
import json
from django.utils.translation import gettext_lazy as _

def load_json_settings(filename):
    """Loads a JSON file and returns the parsed data."""
    file_path = os.path.join(os.path.dirname(__file__), filename)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise RuntimeError(f"Configuration file '{filename}' not found.")
    except json.JSONDecodeError:
        raise RuntimeError(f"Error parsing '{filename}'. Ensure it's a valid JSON file.")

def get_languages():
    """Returns LANGUAGES list from the JSON configuration."""
    language_data = load_json_settings('languages.json')
    return [(lang[0], _(lang[1])) for lang in language_data.get('languages', [])]

def get_parler_languages():
    """Returns PARLER_LANGUAGES dictionary from the JSON configuration."""
    language_data = load_json_settings('languages.json')
    return {
        None: tuple(language_data.get('parler_languages', {}).get('global', [])),
        'default': language_data.get('parler_languages', {}).get('default', {})
    }
