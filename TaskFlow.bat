@echo off
cd /d "%~dp0"
echo Starting TaskFlow...
start /min cmd /c "python app.py"
timeout /t 3 /nobreak > nul
start http://127.0.0.1:5000
echo TaskFlow is running. Close this window to exit.
pause > nul
taskkill /F /IM python.exe /T 