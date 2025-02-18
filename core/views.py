import os
import sys
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view

@swagger_auto_schema(
    method="post",
    operation_description="Securely restarts the Django application.",
    responses={200: openapi.Response("Django is restarting...")},
)
@api_view(["POST"])
@csrf_exempt
@user_passes_test(lambda u: u.is_superuser)  # Only superusers can restart
def restart_django(request):
    """Securely restart Django & work in Swagger + Postman."""

    try:
        if os.environ.get("RUNNING_IN_DOCKER"):
            os.system("touch /app/restart.txt")  # Trigger Docker restart
        else:
            python_executable = sys.executable
            manage_py = os.path.abspath("manage.py")

            print("🔄 Restarting Django...")  #

            # Run Django in a new background process (no immediate exit)
            subprocess.Popen(
                [python_executable, manage_py, "runserver", "0.0.0.0:8000"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,  # Prevents immediate exit
            )

            return JsonResponse({"message": "Django is restarting..."})  # Respond immediately

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
