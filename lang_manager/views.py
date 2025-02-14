from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import load_languages, save_languages, add_language, remove_language, generate_all_translations, generate_translation_files
from .utils import list_rosetta_translations, list_parler_translations # make this later in a separate thingy

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

    return JsonResponse({"error": "Invalid request method"}, status=405)\
    
# TODO: add the below stuff to a separate file 

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