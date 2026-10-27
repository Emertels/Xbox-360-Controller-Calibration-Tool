@echo off
setlocal enabledelayedexpansion
title Instalando Dependencias - Xbox 360 Calibration Tool v1.0.0
cd /d "%~dp0"
echo ========================================================
echo   Instalando dependencias - Xbox 360 Calibration Tool
echo ========================================================
echo.

set "PY_BIN="

if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PY_BIN=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not defined PY_BIN if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" set "PY_BIN=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
if not defined PY_BIN if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" set "PY_BIN=%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
if not defined PY_BIN if exist "C:\Users\Emerson Teles\AppData\Local\Programs\Python\Python312\python.exe" set "PY_BIN=C:\Users\Emerson Teles\AppData\Local\Programs\Python\Python312\python.exe"

if not defined PY_BIN (
    where python >nul 2>&1
    if !ERRORLEVEL! equ 0 set "PY_BIN=python"
)

if not defined PY_BIN (
    where py >nul 2>&1
    if !ERRORLEVEL! equ 0 set "PY_BIN=py -3"
)

if not defined PY_BIN (
    echo [ERRO] Python 3 nao encontrado!
    echo Instale o Python (marcando "Add python.exe to PATH"):
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/2] Verificando versao do Python:
!PY_BIN! --version
echo.

echo [2/2] Instalando dependencias (vgamepad)...
!PY_BIN! -m pip install -r "%~dp0requirements.txt" --upgrade
echo.

if %ERRORLEVEL% equ 0 (
    echo ========================================================
    echo   SUCESSO! Dependencias instaladas perfeitamente.
    echo ========================================================
    echo.
    echo   Agora voce ja pode iniciar a ferramenta clicando em:
    echo     - INICIAR_SEM_CMD.vbs (inicia sem tela preta)
    echo     - INICIAR.bat
    echo.
    echo   Lembre-se: Para criar o controle virtual nos jogos,
    echo   instale tambem o driver oficial ViGEmBus:
    echo   https://github.com/nefarius/ViGEmBus/releases
    echo.
) else (
    echo ========================================================
    echo   Aviso: vgamepad nao pode ser instalado.
    echo ========================================================
    echo.
    echo   A ferramenta de calibracao e diagnostico dos analogicos
    echo   continua funcionando normalmente!
    echo.
)
pause
