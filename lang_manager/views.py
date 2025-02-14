from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import (
    load_languages, add_language, remove_language, generate_all_translations, generate_translation_files,
    list_rosetta_translations, list_parler_translations, update_parler_translation, update_rosetta_translation
)

@csrf_exempt
def list_languages(request):
    """Returns the list of available languages."""
    return JsonResponse(load_languages())

@csrf_exempt
def add_language_view(request):
    """Adds a new language to languages.json."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            code = data.get("code")
            name = data.get("name")

            if not code or not name:
                return JsonResponse({"error": "Code and Name are required"}, status=400)

            if add_language(code, name):
                return JsonResponse({"message": f"Language {name} ({code}) added successfully"})
            else:
                return JsonResponse({"error": "Language already exists"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def remove_language_view(request):
    """Removes a language from languages.json."""
    if request.method == "POST":
        data = json.loads(request.body)
        code = data.get("code")

        if not code:
            return JsonResponse({"error": "Code is required"}, status=400)

        remove_language(code)
        return JsonResponse({"message": f"Language {code} removed successfully"})

@csrf_exempt
def generate_translations_view(request):
    """API endpoint to manually trigger .po and .mo file generation for all languages."""
    if request.method == "POST":
        result = generate_all_translations()
        return JsonResponse({
            "message": "Translation files generated",
            "success": result["success"],
            "failed": result["failed"]
        })

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def generate_translation_for_language(request, lang_code):
    """API endpoint to generate .po and .mo files for a specific language."""
    if request.method == "POST":
        success = generate_translation_files(lang_code)
        if success:
            return JsonResponse({"message": f"Translation files generated for {lang_code}"})
        else:
            return JsonResponse({"error": f"Failed to generate translation files for {lang_code}"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def list_translations_view(request):
    """API endpoint to list all translations from Rosetta and Parler."""
    if request.method == "GET":
        rosetta_translations = list_rosetta_translations()
        parler_translations = list_parler_translations()

        return JsonResponse({
            "rosetta_translations": rosetta_translations,
            "parler_translations": parler_translations
        }, safe=False)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def update_translation_view(request):
    """API endpoint to modify translations for a specific object in Rosetta or Parler."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            translation_type = data.get("type")  # "parler" or "rosetta"

            if translation_type == "parler":
                model_name = data.get("model_name")
                object_id = data.get("object_id")  # ✅ Require object ID
                lang_code = data.get("language_code")
                field = data.get("field")  # Must be "title" or "content"
                new_translation = data.get("new_translation")

                if not all([model_name, object_id, lang_code, field, new_translation]):
                    return JsonResponse({"error": "Missing required parameters"}, status=400)

                success = update_parler_translation(model_name, object_id, lang_code, field, new_translation)

            elif translation_type == "rosetta":
                lang_code = data.get("language_code")
                key = data.get("key")  # The translation key in the .po file
                new_translation = data.get("new_translation")

                if not all([lang_code, key, new_translation]):
                    return JsonResponse({"error": "Missing required parameters"}, status=400)

                success = update_rosetta_translation(lang_code, key, new_translation)

            else:
                return JsonResponse({"error": "Invalid translation type"}, status=400)

            if success:
                return JsonResponse({"message": "Translation updated successfully"})
            else:
                return JsonResponse({"error": "Translation or object not found"}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def batch_update_rosetta_translations(request):
    """API endpoint to batch update multiple translations across multiple languages in Rosetta."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            translations_data = data.get("rosetta_translations", [])  # Default to empty list if missing

            if not isinstance(translations_data, list):
                return JsonResponse({"error": "Invalid data format. 'rosetta_translations' must be a list."}, status=400)

            updated = []
            errors = []

            for language_entry in translations_data:
                lang_code = language_entry.get("language_code")
                translations = language_entry.get("translations", [])
                missing_translations = language_entry.get("missing_translations", [])

                if not isinstance(translations, list) or not isinstance(missing_translations, list):
                    errors.append({"language": lang_code, "error": "'translations' and 'missing_translations' must be lists."})
                    continue

                if not lang_code:
                    errors.append({"error": "Missing language_code in entry."})
                    continue

                # ✅ Process existing translations
                for translation in translations:
                    key = translation.get("original")
                    new_translation = translation.get("translated")
                    if key and new_translation:
                        success = update_rosetta_translation(lang_code, key, new_translation)
                        if success:
                            updated.append({"language": lang_code, "key": key, "new_translation": new_translation})
                        else:
                            errors.append({"language": lang_code, "key": key, "error": "Translation update failed"})

                # ✅ Process missing translations
                for translation in missing_translations:
                    key = translation.get("original")
                    new_translation = translation.get("translated")
                    if key and new_translation:
                        success = update_rosetta_translation(lang_code, key, new_translation)
                        if success:
                            updated.append({"language": lang_code, "key": key, "new_translation": new_translation})
                        else:
                            errors.append({"language": lang_code, "key": key, "error": "Failed to add missing translation"})

            response = {"updated": updated}
            if errors:
                response["errors"] = errors

            return JsonResponse(response)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
