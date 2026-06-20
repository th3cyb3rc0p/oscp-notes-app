#!/usr/bin/env bash
# build_app.sh — build OSCP-Notes.app for macOS via PyInstaller.
#
# Output:
# dist/OSCP-Notes.app (double-clickable, universal-looking arm64)
# dist/OSCP-Notes/ (the underlying binary folder)
#
# Run from the project root:
# bash build_app.sh
#
# After build:
# open dist/OSCP-Notes.app
# # or copy:
# cp -R dist/OSCP-Notes.app /Applications/
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

if [[ "$(uname -s)" != "Darwin" ]]; then
	echo "build_app.sh is macOS-only. On Linux run build_linux.sh, on Windows run build_windows.bat."
	exit 1
fi

# ---- pick a python ----
if [[ -x "$HERE/venv/bin/python" ]]; then
	PY="$HERE/venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
	PY="$(command -v python3)"
else
	echo "python3 not on PATH. Install via Homebrew: brew install python@3.14"
	exit 1
fi

# ---- tkinter check ----
if ! "$PY" -c 'import tkinter' 2>/dev/null; then
	echo "tkinter missing. Install via Homebrew: brew install python-tk@3.14"
	exit 1
fi

# ---- venv ----
if [[ ! -x "$HERE/venv/bin/python" ]]; then
	echo "Creating venv..."
	"$PY" -m venv "$HERE/venv"
fi
PYVENV="$HERE/venv/bin/python"

# ---- deps ----
echo "Installing dependencies..."
"$PYVENV" -m pip install --quiet --upgrade pip
"$PYVENV" -m pip install --quiet -r "$HERE/requirements.txt"
"$PYVENV" -m pip install --quiet pyinstaller

# ---- build ----
echo
echo "Running PyInstaller..."
rm -rf "$HERE/dist" "$HERE/build"
"$PYVENV" -m PyInstaller --noconfirm --clean OSCP-Notes.spec

# ---- done ----
APP="$HERE/dist/OSCP-Notes.app"
echo
echo "Built: $APP"
echo "Run: open \"$APP\""
echo "Install: cp -R \"$APP\" /Applications/"
du -sh "$APP"