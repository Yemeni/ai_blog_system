import os
import sys
import subprocess
from django.contrib.auth.decorators import user_passes_test
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


# --------------------------------------
# 📌 Secure Django Restart API
# --------------------------------------
@swagger_auto_schema(
    method="post",
    operation_description="Securely restarts the Django application. Requires admin privileges.",
    responses={
        200: openapi.Response("Django is restarting..."),
        403: openapi.Response("Forbidden: Only superusers can restart Django."),
        500: openapi.Response("Server error while restarting Django."),
    }
)
@api_view(["POST"])
@user_passes_test(lambda u: u.is_superuser)  # Only superusers can restart Django
def restart_django(request):
    """Securely restart the Django application."""

    try:
        if os.environ.get("RUNNING_IN_DOCKER"):
            os.system("touch /app/restart.txt")  # Docker restart trigger
        else:
            # Restart Django without breaking debugging
            subprocess.Popen([sys.executable, "manage.py", "runserver", "0.0.0.0:8000"])

            # Exit the old process
            os._exit(0)

        return Response({"message": "Django is restarting..."})

    except Exception as e:
        return Response({"error": str(e)}, status=500)