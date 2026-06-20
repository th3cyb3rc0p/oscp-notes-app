# Building OSCP-Notes

All three platforms use PyInstaller driven by the single `OSCP-Notes.spec` file in this directory.

## Why a spec file?

All three build scripts call PyInstaller with `--clean OSCP-Notes.spec`. That keeps the binary layout, hidden imports, and bundle metadata identical across macOS, Linux, and Windows — only the per-OS wrapper (`.app`, `.desktop`, `.exe`) differs.

## Build on each OS

The build scripts bootstrap everything for you: venv, dependencies, PyInstaller, build. They all take ~30 seconds on a modern machine.

### macOS
```bash
bash build_app.sh
open dist/OSCP-Notes.app
# or install: cp -R dist/OSCP-Notes.app /Applications/
```
Output: `dist/OSCP-Notes.app` (60 MB, double-clickable from Finder).

### Linux
```bash
# First time only — Tk runtime dep
sudo apt install python3-tk # Debian/Ubuntu/Kali/Parrot
# sudo dnf install python3-tkinter # Fedora/RHEL
# sudo pacman -S tk # Arch

bash build_linux.sh
./dist/OSCP-Notes/OSCP-Notes
```
Output: `dist/OSCP-Notes/` containing the executable + bundled Python + a matching `OSCP-Notes.desktop` file. Optional: copy the `.desktop` file to `~/.local/share/applications/` to make it show up in your application launcher.

### Windows
```cmd
:: from cmd.exe in the project folder
build_windows.bat
:: or for a single .exe (slower first launch, easier to share):
build_windows_onefile.bat

:: run
dist\OSCP-Notes\OSCP-Notes.exe
```
Output:
- Folder build: `dist\OSCP-Notes\OSCP-Notes.exe` (60 MB, launches immediately)
- Single-file build: `dist\OSCP-Notes.exe` (30 MB, extracts on launch)

## Dispatcher

`bash build_all.sh` picks the right script for the current host. On Windows shells it just prints the cmd to run.

## Cross-compilation

PyInstaller does not support cross-compilation. Each binary must be built on its target OS — that's why the macOS bundle ships from this repo and the Windows/Linux binaries come from running `build_windows.bat` / `build_linux.sh` on their respective hosts.

If you only have a Mac and want a Windows binary, options are:
- Ask someone with a Windows box to clone the repo and run `build_windows.bat`.
- Use a Windows VM (VirtualBox, Parallels, UTM with Windows ARM) and run the script.
- Use a CI runner (GitHub Actions has free Windows + Linux runners).

## What's inside the bundle

`dist/OSCP-Notes.app/Contents/Frameworks/` (or `dist/OSCP-Notes/_internal/` on Linux, `dist\OSCP-Notes\_internal\` on Windows) contains:
- `libpython3.14.dylib` / `python314.dll` / `libpython3.14.so` — the embedded interpreter
- `tkinter` / Tk runtime
- `reportlab`, `openpyxl`, `cryptography`, `markdown`, `pygments` — every `pip install -r requirements.txt` dep
- `cheatseeds` and `oscp_practice_list` modules — bundled by PyInstaller

## Rebuilding

To rebuild after a code change:
```bash
rm -rf build dist
bash build_app.sh # or build_linux.sh / build_windows.bat
```

Your data folder (`~/OSCP-Notes/` etc.) is never touched by a rebuild.