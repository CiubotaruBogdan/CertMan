@echo off
REM Script de pornire pentru Manager Certificate Securitate - Windows

echo ========================================
echo Manager Certificate Securitate
echo ========================================
echo.

REM Verifică dacă Python este instalat
python --version >nul 2>&1
if errorlevel 1 (
    echo EROARE: Python nu este instalat sau nu este in PATH
    echo.
    echo Descarcati Python de la: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Pornește aplicația
echo Pornire aplicatie...
echo.
python main.py

REM Dacă aplicația se închide cu eroare, afișează mesaj
if errorlevel 1 (
    echo.
    echo EROARE: Aplicatia s-a inchis cu erori
    echo.
    pause
)
