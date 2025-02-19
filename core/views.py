import os
import sys
import time
import subprocess
import signal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from django.core.cache import cache


@swagger_auto_schema(
    method="post",
    operation_description="Fully restarts Django WSGI application, ensuring settings reload.",
    responses={200: openapi.Response("WSGI server is restarting...")},
)
@api_view(["POST"])
@csrf_exempt
@user_passes_test(lambda u: u.is_superuser)  # Only superusers can restart
def restart_wsgi(request):
    """Force Django WSGI restart, ensuring settings reload."""
    try:
        cache.clear()  # ✅ Clear Django cache before restart
        print("🔄 Restarting WSGI server...")

        # ✅ Check if running inside Docker
        if os.environ.get("RUNNING_IN_DOCKER"):
            os.system("touch /app/restart.txt")  # 🔄 Docker restart trigger

        else:
            # ✅ 1. Touch wsgi.py to trigger reload
            wsgi_file = os.path.abspath("AI_Blog_System/wsgi.py")
            os.utime(wsgi_file, None)

            # ✅ 2. Kill the current Django process
            pid = os.getpid()
            print(f"🔴 Stopping Django process {pid}...")
            time.sleep(1)  # Prevent race conditions
            os.kill(pid, signal.SIGTERM)  # Terminate the process

            # ✅ 3. Start Django again (only in runserver mode)
            if "RUNSERVER" in os.environ:
                print("🚀 Restarting Django runserver...")
                python_executable = sys.executable
                manage_py = os.path.abspath("manage.py")

                subprocess.Popen(
                    [python_executable, manage_py, "runserver", "0.0.0.0:8000"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True,  # Prevents immediate exit
                )

        return JsonResponse({"message": "WSGI server is restarting..."})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
