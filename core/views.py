import os
import subprocess
import platform
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from django.core.cache import cache

@swagger_auto_schema(
    method="post",
    operation_description="Restarts Django (supports Docker & non-Docker).",
    responses={200: openapi.Response("Django is restarting...")},
)
@api_view(["POST"])
@csrf_exempt
@user_passes_test(lambda u: u.is_superuser)  # Only superusers can restart
def restart_wsgi(request):
    """Restart Django using a shell script or Docker trigger."""
    try:
        cache.clear() 
        print("🔄 Running restart script...")

        # ✅ Detect if running inside Docker
        if os.environ.get("RUNNING_IN_DOCKER"):
            print("🐳 Restarting Django inside Docker...")
            os.system("touch /app/restart.txt")  # Docker-specific reload
        else:
            system_type = platform.system()
            if system_type == "Windows":
                script_path = os.path.abspath("restart_django.ps1")
                subprocess.Popen(
                    ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", script_path],
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            else:  # Linux/macOS
                script_path = os.path.abspath("restart_django.sh")
                subprocess.Popen(
                    ["/bin/bash", script_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )

        return JsonResponse({"message": "Django restart initiated. Check logs for confirmation."})

    except Exception as e:
        return JsonResponse({"error": "Restart failed", "details": str(e)}, status=500)
