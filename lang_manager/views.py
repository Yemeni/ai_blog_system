from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .utils import (
    load_languages, add_language, remove_language, generate_all_translations, generate_translation_files,
    list_rosetta_translations, list_parler_translations, update_parler_translation, update_rosetta_translation
)


# --------------------------------------
# 📌 List Available Languages
# --------------------------------------
@swagger_auto_schema(
    method="get",
    operation_description="Returns the list of available languages.",
    responses={200: openapi.Response("List of languages")}
)
@api_view(["GET"])
def list_languages(request):
    """Returns the list of available languages."""
    return Response(load_languages())


# --------------------------------------
# 📌 Add a New Language
# --------------------------------------
@swagger_auto_schema(
    method="post",
    operation_description="Adds a new language to the system.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "code": openapi.Schema(type=openapi.TYPE_STRING, example="zh-hans"),
            "name": openapi.Schema(type=openapi.TYPE_STRING, example="Chinese"),
        },
        required=["code", "name"],
    ),
    responses={200: openapi.Response("Language added successfully")}
)
@api_view(["POST"])
def add_language_view(request):
    """Adds a new language to languages.json."""
    data = request.data
    code = data.get("code")
    name = data.get("name")

    if not code or not name:
        return Response({"error": "Code and Name are required"}, status=400)

    if add_language(code, name):
        return Response({"message": f"Language {name} ({code}) added successfully"})

    return Response({"error": "Language already exists"}, status=400)


# --------------------------------------
# 📌 Remove a Language
# --------------------------------------
@swagger_auto_schema(
    method="post",
    operation_description="Removes a language from the system.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "code": openapi.Schema(type=openapi.TYPE_STRING, example="zh-hans"),
        },
        required=["code"],
    ),
    responses={200: openapi.Response("Language removed successfully")}
)
@api_view(["POST"])
def remove_language_view(request):
    """Removes a language from languages.json."""
    code = request.data.get("code")

    if not code:
        return Response({"error": "Code is required"}, status=400)

    remove_language(code)
    return Response({"message": f"Language {code} removed successfully"})


# --------------------------------------
# 📌 Generate All Translations
# --------------------------------------
@swagger_auto_schema(
    method="post",
    operation_description="Generates .po and .mo files for all languages.",
    responses={200: openapi.Response("Translation files generated")}
)
@api_view(["POST"])
def generate_translations_view(request):
    """API endpoint to manually trigger .po and .mo file generation for all languages."""
    result = generate_all_translations()
    return Response({
        "message": "Translation files generated",
        "success": result["success"],
        "failed": result["failed"]
    })


# --------------------------------------
# 📌 Generate Translation for a Specific Language
# --------------------------------------
@swagger_auto_schema(
    method="post",
    operation_description="Generates .po and .mo files for a specific language.",
    responses={200: openapi.Response("Translation files generated for the language")}
)
@api_view(["POST"])
def generate_translation_for_language(request, lang_code):
    """API endpoint to generate .po and .mo files for a specific language."""
    success = generate_translation_files(lang_code)
    if success:
        return Response({"message": f"Translation files generated for {lang_code}"})
    return Response({"error": f"Failed to generate translation files for {lang_code}"}, status=500)


# --------------------------------------
# 📌 List Translations
# --------------------------------------
@swagger_auto_schema(
    method="get",
    operation_description="Lists all translations from Rosetta and Parler.",
    responses={200: openapi.Response("Translation list")}
)
@api_view(["GET"])
def list_translations_view(request):
    """API endpoint to list all translations from Rosetta and Parler."""
    return Response({
        "rosetta_translations": list_rosetta_translations(),
        "parler_translations": list_parler_translations()
    })


# --------------------------------------
# 📌 Update a Translation
# --------------------------------------
@swagger_auto_schema(
    method="post",
    operation_description="Updates a specific translation in Rosetta or Parler.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "type": openapi.Schema(type=openapi.TYPE_STRING, example="rosetta"),
            "language_code": openapi.Schema(type=openapi.TYPE_STRING, example="fr"),
            "key": openapi.Schema(type=openapi.TYPE_STRING, example="title"),
            "new_translation": openapi.Schema(type=openapi.TYPE_STRING, example="Le Titre"),
        },
        required=["type", "language_code", "key", "new_translation"],
    ),
    responses={200: openapi.Response("Translation updated successfully")}
)
@api_view(["POST"])
def update_translation_view(request):
    """API endpoint to modify translations for a specific object in Rosetta or Parler."""
    data = request.data
    translation_type = data.get("type")

    if translation_type == "parler":
        success = update_parler_translation(
            data.get("model_name"),
            data.get("object_id"),
            data.get("language_code"),
            data.get("field"),
            data.get("new_translation")
        )

    elif translation_type == "rosetta":
        success = update_rosetta_translation(
            data.get("language_code"),
            data.get("key"),
            data.get("new_translation")
        )

    else:
        return Response({"error": "Invalid translation type"}, status=400)

    if success:
        return Response({"message": "Translation updated successfully"})
    return Response({"error": "Translation or object not found"}, status=404)


# --------------------------------------
# 📌 Batch Update Rosetta Translations
# --------------------------------------
@swagger_auto_schema(
    method="post",
    operation_description="Batch update multiple translations across multiple languages in Rosetta.",
    responses={200: openapi.Response("Batch translation update successful")}
)
@api_view(["POST"])
def batch_update_rosetta_translations(request):
    """API endpoint to batch update multiple translations across multiple languages in Rosetta."""
    data = request.data.get("rosetta_translations", [])

    if not isinstance(data, list):
        return Response({"error": "Invalid data format. 'rosetta_translations' must be a list."}, status=400)

    updated = []
    errors = []

    for entry in data:
        lang_code = entry.get("language_code")
        translations = entry.get("translations", [])
        missing_translations = entry.get("missing_translations", [])

        for translation in translations + missing_translations:
            success = update_rosetta_translation(lang_code, translation.get("original"), translation.get("translated"))
            if success:
                updated.append({"language": lang_code, "key": translation.get("original"),
                                "new_translation": translation.get("translated")})
            else:
                errors.append({"language": lang_code, "key": translation.get("original"),
                               "error": "Failed to update translation"})

    return Response({"updated": updated, "errors": errors if errors else None})
