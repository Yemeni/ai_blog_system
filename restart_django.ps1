# Stop running Django process
$django = Get-Process -Name "python" -ErrorAction SilentlyContinue
if ($django) {
    Stop-Process -Id $django.Id -Force
    Start-Sleep -Seconds 2
}

# Start Django again
Start-Process -NoNewWindow -FilePath ".venv\Scripts\python.exe" `
    -ArgumentList "manage.py", "runserver", "0.0.0.0:8000" `
    -WorkingDirectory "C:\Users\yhadh\PycharmProjects\AI_Blog_System"
