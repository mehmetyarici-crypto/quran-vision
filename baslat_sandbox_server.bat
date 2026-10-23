@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================================================
echo   [SANDBOX] QURAN VISION TEST ORTAMI (v6.3.0-beta.1 ^| localhost:8080)
echo   Klasor : %~dp0docs
echo   Adres  : http://localhost:8080
echo ============================================================================
start http://localhost:8080
python -m http.server 8080 --directory docs
pause
