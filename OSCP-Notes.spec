# -*- mode: python ; coding: utf-8 -*-
# OSCP-Notes.spec — single source of truth for the PyInstaller build.
# All three platform build scripts (build_app.sh, build_linux.sh, build_windows.bat)
# drive PyInstaller with this spec. The only thing that changes per OS is the
# windowed/console flag and the icon path (none for now).

import sys
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

a = Analysis(
 ['oscp_notes.py'],
 pathex=[],
 binaries=[],
 datas=collect_data_files('pygments'),
 hiddenimports=[
 'reportlab',
 'openpyxl',
 'cryptography',
 'cryptography.hazmat.primitives.kdf.scrypt',
 'cryptography.fernet',
 'PIL', # pulled in by reportlab for image tests
 ],
 hookspath=[],
 hooksconfig={},
 runtime_hooks=[],
 excludes=[
 # Trim what we don't need to shrink the binary a bit
 'test', 'tests', 'unittest', 'pydoc',
 'numpy', 'pandas', 'matplotlib', 'scipy',
 ],
 win_no_prefer_redirects=False,
 win_private_assemblies=False,
 cipher=block_cipher,
 noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Decide per-OS: on macOS and Windows we want a windowed app (no terminal
# window). On Linux, windowed is meaningless (no concept of a console window)
# so we leave it off and let the app just run from the binary.
exe = EXE(
 pyz,
 a.scripts,
 [],
 exclude_binaries=True,
 name='OSCP-Notes',
 debug=False,
 bootloader_ignore_signals=False,
 strip=False,
 upx=False,
 console=False, # windowed
 disable_windowed_traceback=False,
 argv_emulation=False,
 target_arch=None,
 codesign_identity=None,
 entitlements_file=None,
)

# Fold everything into one folder so the binary + deps travel together.
coll = COLLECT(
 exe,
 a.binaries,
 a.zipfiles,
 a.datas,
 strip=False,
 upx=False,
 upx_exclude=[],
 name='OSCP-Notes',
)

# On macOS, also wrap into a .app bundle for double-clickable launch.
if sys.platform == 'darwin':
 app = BUNDLE(
 coll,
 name='OSCP-Notes.app',
 icon=None,
 bundle_identifier='local.oscp.notes',
 info_plist={
 'CFBundleName': 'OSCP Notes',
 'CFBundleDisplayName': 'OSCP Notes',
 'CFBundleVersion': '1.1',
 'CFBundleShortVersionString': '1.1',
 'LSMinimumSystemVersion': '13.0',
 'NSHighResolutionCapable': True,
 'NSPrincipalClass': 'NSApplication',
 },
 )