@echo off
cd /d "%~dp0"

echo Vaalikoneen aineiston tuonti
echo ============================
echo.

python create_import_json.py

if errorlevel 1 (
    echo.
    echo VIRHE: Tuonti ei onnistunut.
    echo Ota virheilmoituksesta kuva ja toimita se tekniselle yllapidolle.
) else (
    echo.
    echo Tuonti valmis.
    echo Tiedosto candidates_import.json on luotu tahan kansioon.
)

echo.
pause