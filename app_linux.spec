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

from PyInstaller.utils.hooks import collect_all, copy_metadata

# Collect all numpy and pandas components properly
numpy_datas, numpy_binaries, numpy_hiddenimports = collect_all('numpy')
pandas_datas, pandas_binaries, pandas_hiddenimports = collect_all('pandas')

a = Analysis(
    [os.path.join(src_root, 'main.py')],  # Your main script
    pathex=[src_root],
    binaries=numpy_binaries + pandas_binaries,
    datas=[
        (os.path.join(assets_root, 'icon.png'), 'assets'),  # Include icon (PNG for Linux)
        *kv_files,  # Include all found .kv files
        *numpy_datas,
        *pandas_datas,
        *copy_metadata('numpy'),
        *copy_metadata('pandas'),
    ],
    hiddenimports=[
        'kivy',
        'kivymd',
        'openpyxl',
        'tkinter',
        'tkinter.filedialog',
        *numpy_hiddenimports,
        *pandas_hiddenimports,
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[os.path.join(spec_root, 'hook-numpy.py')],
    excludes=[
        'numpy.core.tests',
        'numpy.tests',
        'pandas.tests',
    ],
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
    name='MyJongg-Calculator',
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
    icon=os.path.join(assets_root, 'icon.png')
)


