#!/usr/bin/env bash
# build_all.sh — dispatch to the right per-OS build script.
# Use this from a fresh checkout; it picks the correct builder for the host OS.
#
# macOS -> bash build_app.sh (produces OSCP-Notes.app)
# Linux -> bash build_linux.sh (produces dist/OSCP-Notes/)
# Windows -> run build_windows.bat from cmd.exe (produces dist\OSCP-Notes\OSCP-Notes.exe)
set -euo pipefail

UNAME_S="$(uname -s)"
HERE="$(cd "$(dirname "$0")" && pwd)"

case "$UNAME_S" in
	Darwin)
		echo "[build_all] macOS detected -> build_app.sh"
		exec bash "$HERE/build_app.sh" ;;
	Linux)
		echo "[build_all] Linux detected -> build_linux.sh"
		exec bash "$HERE/build_linux.sh" ;;
	MINGW*|MSYS*|CYGWIN*)
		echo "[build_all] Windows shell detected -> run build_windows.bat from cmd.exe"
		echo " cd \"$HERE\" && build_windows.bat"
		echo " # or for a single .exe: build_windows_onefile.bat"
		exit 0 ;;
	*)
		echo "[build_all] Unknown OS: $UNAME_S"
		echo " macOS : bash build_app.sh"
		echo " Linux : bash build_linux.sh"
		echo " Windows : build_windows.bat"
		exit 1 ;;
esac