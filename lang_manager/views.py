from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import load_languages, save_languages, add_language, remove_language

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
