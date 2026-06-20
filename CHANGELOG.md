# Changelog

All notable changes to OSCP Notes are documented in this file.

## [1.1] - 2026-06-19

### Added
- Four-tab UI: **Notes**, **Tracker**, **Payloads**, **Vault**
- Per-machine exam tracker (timer, status, methodology checklist with progress, creds, loot, screenshots, flags)
- Searchable payload library seeded with 35 common payloads
- AES-encrypted vault (Fernet + scrypt-derived master password)
- Reveal-for-N-seconds vault button to limit accidental exposure
- Report shell generator that parses flags / creds / hashes / headings and emits a 10-section Markdown skeleton
- Multi-format bulk export — CSV / JSON / XLSX / PDF
- Cross-platform builds (macOS .app, Linux folder + .desktop, Windows .exe via PyInstaller)
- 4 themes: OSCP Dark (default), Hack The Box, TryHackMe, Light
- LainKusanagi OSCP practice list seeded on first run

### Changed
- Tk font defaults switched from macOS-only (`Menlo`, `Helvetica Neue`) to platform-appropriate fallbacks (`Consolas`/`Segoe UI`/`DejaVu Sans` family)
- Keybindings bind both `<Command-*>` and `<Control-*>` so shortcuts work on all OSes
- Menu accelerators display as `Ctrl+N` etc. on Win/Linux instead of `Cmd+N`
- Data folder now resolves per platform (`~/OSCP-Notes/` on macOS, `$XDG_DATA_HOME/OSCP-Notes/` on Linux, `%APPDATA%\OSCP-Notes\` on Windows)
- PDF export picks the first available system font (Menlo / Consolas / Courier New / DejaVu Sans Mono) before falling back to Courier

## [1.0]

Initial release.

- Markdown editor with live preview and Pygments syntax highlighting
- Phase tags, free-form tags, full-text search (SQLite FTS5)
- Built-in cheat sheets (Reverse Shells, Linux/Windows PrivEsc, AD, BoF, Pivoting, Web Enum, File Transfer, Web Shells, One-Liners)
- macOS-native menu bar
- Auto-save
- Theme preference persistence
