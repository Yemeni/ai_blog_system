import os
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from django.core.cache import cache

@swagger_auto_schema(
    method="post",
    operation_description="Restarts Django using an external shell script.",
    responses={200: openapi.Response("Django is restarting...")},
)
@api_view(["POST"])
@csrf_exempt
@user_passes_test(lambda u: u.is_superuser)  # Only superusers can restart
def restart_wsgi(request):
    """Restart Django using a shell script."""
    try:
        cache.clear()  # Clear Django cache before restart
        print("🔄 Running restart script...")

        script_path = os.path.abspath("restart_django.sh")

        # Execute shell script (ensure it's executable: chmod +x restart_django.sh)
        subprocess.Popen(["/bin/bash", script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        return JsonResponse({"message": "Django is restarting..."})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
