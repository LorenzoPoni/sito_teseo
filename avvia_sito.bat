@echo off
cd /d "%~dp0"
echo Avvio server...
echo Il sara disponibile su http://localhost:3000
echo Premi Ctrl+C per fermare il server
echo.
node server.js
pause
