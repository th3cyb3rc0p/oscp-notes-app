@echo off
REM build_windows.bat - build OSCP-Notes.exe for Windows via PyInstaller.
REM
REM Output:
REM dist\OSCP-Notes\OSCP-Notes.exe (the binary)
REM dist\OSCP-Notes\ (folder with bundled Python + Tk + deps)
REM
REM Run from cmd.exe in this folder:
REM build_windows.bat
REM
REM End-user usage:
REM dist\OSCP-Notes\OSCP-Notes.exe
REM
REM To distribute as a single .exe, run build_windows_onefile.bat instead.
setlocal enabledelayedexpansion

set HERE=%~dp0
cd /d "%HERE%"

REM ---- pick a python ----
set PY=python
where python 1>nul 2>nul
if errorlevel 1 (
 echo Python not on PATH. Install Python 3.11+ from https://python.org
 exit /b 1
)

REM ---- tkinter check (python.org installer includes it by default) ----
"%PY%" -c "import tkinter" 1>nul 2>nul
if errorlevel 1 (
 echo tkinter missing. Reinstall Python and tick "tcl/tk and IDLE" in the installer.
 exit /b 1
)

REM ---- venv ----
if not exist "venv\Scripts\python.exe" (
 echo Creating venv...
 "%PY%" -m venv venv
)
set PYVENV=%HERE%venv\Scripts\python.exe

REM ---- deps ----
echo Installing dependencies...
"%PYVENV%" -m pip install --quiet --upgrade pip
"%PYVENV%" -m pip install --quiet -r requirements.txt
"%PYVENV%" -m pip install --quiet pyinstaller

REM ---- build ----
echo.
echo Running PyInstaller...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
"%PYVENV%" -m PyInstaller --noconfirm --clean OSCP-Notes.spec

if errorlevel 1 (
 echo.
 echo Build failed.
 exit /b 1
)

echo.
echo Built: %HERE%dist\OSCP-Notes\OSCP-Notes.exe
echo Run: "%HERE%dist\OSCP-Notes\OSCP-Notes.exe"
endlocal