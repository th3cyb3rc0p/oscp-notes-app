@echo off
REM build_windows_onefile.bat - build a single-file OSCP-Notes.exe.
REM Same as build_windows.bat but produces one .exe (~30 MB) instead of a folder.
REM Slightly slower to launch (extracts to a temp dir on run), easier to share.
setlocal enabledelayedexpansion

set HERE=%~dp0
cd /d "%HERE%"

set PY=python
where python 1>nul 2>nul
if errorlevel 1 (
 echo Python not on PATH. Install Python 3.11+ from https://python.org
 exit /b 1
)

"%PY%" -c "import tkinter" 1>nul 2>nul
if errorlevel 1 (
 echo tkinter missing. Reinstall Python and tick "tcl/tk and IDLE" in the installer.
 exit /b 1
)

if not exist "venv\Scripts\python.exe" (
 "%PY%" -m venv venv
)
set PYVENV=%HERE%venv\Scripts\python.exe

echo Installing dependencies...
"%PYVENV%" -m pip install --quiet --upgrade pip
"%PYVENV%" -m pip install --quiet -r requirements.txt
"%PYVENV%" -m pip install --quiet pyinstaller

echo.
echo Running PyInstaller (--onefile)...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
"%PYVENV%" -m PyInstaller --noconfirm --clean --onefile --name OSCP-Notes oscp_notes.py

if errorlevel 1 (
 echo.
 echo Build failed.
 exit /b 1
)

echo.
echo Built: %HERE%dist\OSCP-Notes.exe
echo Run: "%HERE%dist\OSCP-Notes.exe"
endlocal