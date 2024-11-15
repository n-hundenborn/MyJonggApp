from kivy_deps import sdl2, glew
import os
import glob
# Define paths using absolute paths
spec_root = os.path.abspath('.')  # Current directory
src_root = os.path.join(spec_root, 'src')
assets_root = os.path.join(spec_root, 'assets')
# Find all .kv files in the project
kv_files = []
for root, dirs, files in os.walk(src_root):
    for file in files:
        if file.endswith('.kv'):
            source_path = os.path.join(root, file)
            # Calculate relative path from src_root
            rel_path = os.path.relpath(os.path.dirname(source_path), src_root)
            kv_files.append((source_path, rel_path))
a = Analysis(
    [os.path.join(src_root, 'main.py')],  # Your main script
    pathex=[src_root],
    binaries=[],
    datas=[
        (os.path.join(assets_root, 'icon.ico'), 'assets'),  # Include icon
        *kv_files,  # Include all found .kv files
    ],
    hiddenimports=[
        'kivy',
        'kivymd',
        'pandas',
        'openpyxl',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False
)
pyz = PYZ(a.pure, a.zipped_data)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    name='MyJongg Calculator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(assets_root, 'icon.ico')
)
