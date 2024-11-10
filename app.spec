from kivy_deps import sdl2, glew
import os

# Define paths using absolute paths
spec_root = os.path.abspath('.')
src_root = os.path.join(spec_root, 'src')
assets_root = os.path.join(spec_root, 'assets')

a = Analysis(
    [os.path.join(src_root, 'main.py')],
    pathex=[src_root],
    binaries=[],
    datas=[
        (os.path.join(assets_root, 'icon.ico'), 'assets'),
    ],
    hiddenimports=[
        'kivy',
        'kivymd',
        'pandas',
        'openpyxl',
    ],
    # Exclude unnecessary packages
    excludes=[
        'matplotlib', 'notebook', 'scipy', 'tk', 'tkinter', 
        'PIL', 'PyQt5', 'PyQt6', 'PySide2', 'PySide6',
        'IPython', 'jupyter', 'sqlite3', 'email', 'html', 'http',
        'pkg_resources', 'unittest', 'xml', 'doctest', 'pdb',
        'pydoc', 'pytest'
    ],
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
    name='Myjongg Calculator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,  # Strip symbols from binaries
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(assets_root, 'icon.ico')
) 