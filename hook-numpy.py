"""
Runtime hook for numpy to prevent source directory detection issue.
"""
import sys
import os

# Remove any numpy source markers that might confuse the import
if hasattr(sys, '_MEIPASS'):
    # We're running in a PyInstaller bundle
    # Ensure numpy doesn't think it's being imported from source
    for key in list(sys.modules.keys()):
        if key.startswith('numpy'):
            del sys.modules[key]

