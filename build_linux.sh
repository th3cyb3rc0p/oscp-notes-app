#!/usr/bin/env bash
# build_linux.sh — build OSCP-Notes for Linux via PyInstaller.
#
# Output:
# dist/OSCP-Notes/ (binary + bundled Python + .desktop launcher)
# dist/OSCP-Notes/OSCP-Notes (the executable)
#
# Run from the project root:
# bash build_linux.sh
#
# End-user usage:
# ./dist/OSCP-Notes/OSCP-Notes
# # or install the .desktop launcher:
# cp dist/OSCP-Notes/OSCP-Notes.desktop ~/.local/share/applications/
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

if [[ "$(uname -s)" != "Linux" ]]; then
	echo "build_linux.sh is Linux-only. On macOS run build_app.sh, on Windows run build_windows.bat."
	exit 1
fi

# ---- pick a python ----
if [[ -x "$HERE/venv/bin/python" ]]; then
	PY="$HERE/venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
	PY="$(command -v python3)"
else
	echo "python3 not on PATH. Install via your package manager."
	exit 1
fi

PY_VER="$("$PY" -c 'import sys; print("%d.%d" % sys.version_info[:2])')"
PY_MAJOR="${PY_VER%.*}"
PY_MINOR="${PY_VER#*.}"
if [[ "$PY_MAJOR" -lt 3 || ("$PY_MAJOR" -eq 3 && "$PY_MINOR" -lt 11) ]]; then
	echo "Python $PY_VER is too old. Need 3.11+."
	exit 1
fi

# ---- tkinter (Tk) check — must be present at runtime too ----
if ! "$PY" -c 'import tkinter' 2>/dev/null; then
	echo "tkinter is missing. Install it for your distro, e.g.:"
	echo " Debian/Ubuntu/Kali/Parrot : sudo apt install python3-tk"
	echo " Fedora / RHEL / Rocky : sudo dnf install python3-tkinter"
	echo " Arch : sudo pacman -S tk"
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

# ---- write a .desktop launcher next to the binary ----
APPIMAGE_DIR="$HERE/dist/OSCP-Notes"
DESKTOP="$APPIMAGE_DIR/OSCP-Notes.desktop"
cat > "$DESKTOP" <<DESKTOP
[Desktop Entry]
Type=Application
Name=OSCP Notes
GenericName=Pentest note-taking
Comment=Markdown notes, payload library, vault, and exam tracker
Exec=$APPIMAGE_DIR/OSCP-Notes %F
Icon=$APPIMAGE_DIR/OSCP-Notes
Terminal=false
Categories=Utility;Security;Office;
StartupNotify=true
DESKTOP
chmod +x "$APPIMAGE_DIR/OSCP-Notes" "$DESKTOP"

echo
echo "Built: $APPIMAGE_DIR/OSCP-Notes"
echo " $DESKTOP"
echo
echo "Run: \"$APPIMAGE_DIR/OSCP-Notes\""
echo "Or: xdg-open \"$DESKTOP\" (installs the .desktop launcher)"
echo
echo "Note: the app stores data under \$XDG_DATA_HOME/OSCP-Notes"
echo " (default: ~/.local/share/OSCP-Notes)."
du -sh "$APPIMAGE_DIR"