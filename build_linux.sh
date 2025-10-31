#!/bin/bash

echo "Building MyJongg Calculator for Linux..."
echo ""

# Clean previous builds
rm -rf build dist

# Build the executable
pyinstaller --log-level=INFO app_linux.spec

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "Build successful!"
    echo "Executable location: dist/MyJongg-Calculator"
    echo "========================================"
    chmod +x dist/MyJongg-Calculator
else
    echo ""
    echo "========================================"
    echo "Build failed! Check errors above."
    echo "========================================"
    exit 1
fi


