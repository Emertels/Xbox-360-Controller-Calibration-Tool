@echo off
setlocal
cd /d "%~dp0"

:: 1. Tenta pythonw em caminhos comuns do AppData
if exist "%LOCALAPPDATA%\Programs\Python\Python312\pythonw.exe" (
    start "" "%LOCALAPPDATA%\Programs\Python\Python312\pythonw.exe" "%~dp0main.py"
    exit /b 0
)
if exist "%LOCALAPPDATA%\Programs\Python\Python313\pythonw.exe" (
    start "" "%LOCALAPPDATA%\Programs\Python\Python313\pythonw.exe" "%~dp0main.py"
    exit /b 0
)
if exist "%LOCALAPPDATA%\Programs\Python\Python311\pythonw.exe" (
    start "" "%LOCALAPPDATA%\Programs\Python\Python311\pythonw.exe" "%~dp0main.py"
    exit /b 0
)
if exist "C:\Users\Emerson Teles\AppData\Local\Programs\Python\Python312\pythonw.exe" (
    start "" "C:\Users\Emerson Teles\AppData\Local\Programs\Python\Python312\pythonw.exe" "%~dp0main.py"
    exit /b 0
)

:: 2. Tenta pythonw no PATH
where pythonw >nul 2>&1
if %ERRORLEVEL% equ 0 (
    start "" pythonw "%~dp0main.py"
    exit /b 0
)

:: 3. Tenta pyw launcher
where pyw >nul 2>&1
if %ERRORLEVEL% equ 0 (
    start "" pyw -3 "%~dp0main.py"
    exit /b 0
)

:: 4. Fallback python normal
where python >nul 2>&1
if %ERRORLEVEL% equ 0 (
    start "" python "%~dp0main.py"
    exit /b 0
)

echo [ERRO] Python 3 nao foi encontrado no sistema!
echo Por favor, instale o Python marcando a opcao "Add python.exe to PATH":
echo https://www.python.org/downloads/
pause
exit /b 1
