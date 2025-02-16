import os
import sys
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test

@csrf_exempt
def restart_django(request):
    """Restart Django application."""
    if request.method == "GET":
        return JsonResponse({"message": "Use POST to restart Django."})

    if request.method == "POST":
        try:
            if os.environ.get("RUNNING_IN_DOCKER"):
                os.system("touch /app/restart.txt")  # ✅ Docker restart trick
            else:
                # ✅ Restart Django without breaking debugging
                subprocess.Popen([sys.executable, "manage.py", "runserver", "0.0.0.0:8000"])

                # ✅ Exit the old process
                os._exit(0)

            return JsonResponse({"message": "Django is restarting..."})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
