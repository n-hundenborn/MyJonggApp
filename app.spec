# -*- mode: python ; coding: utf-8 -*-
from kivy_deps import sdl2, glew
import os

block_cipher = None

a = Analysis(
    ['src\\main.py'],
    pathex=[os.path.abspath('src')],
    binaries=[],
    datas=[
        ('src\\game.kv', '.'),
        ('assets', 'assets'),
    ],
    hiddenimports=[
        'kivy.core.window.window_sdl2',
        'pkg_resources.py2_warn',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    name='MyJonggApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True if you want a console window for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets\\icon.ico',
)

# Comment out COLLECT section for single-file executable
# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     name='app',
# )

