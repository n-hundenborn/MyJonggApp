# MyJongg Calculator

Cross-platform Mahjongg score calculator built with Kivy.

## 📥 Download Pre-Built Executables

**Don't want to build from source?** Download ready-to-run executables from the [Releases page](../../releases).

- **Windows**: Download `.zip`, extract, run the executable.

## Windows Installation Guide

### Prerequisites
- Windows 10 or 11
- Python 3.12 or higher ([Download from python.org](https://www.python.org/downloads/))
  - ✅ Make sure to check "Add Python to PATH" during installation

### Building the Executable (Windows)

#### Prerequisites
Make sure you have PyInstaller installed:
```cmd
pip install pyinstaller
```

Also install Windows-specific Kivy dependencies:
```cmd
pip install kivy_deps.sdl2 kivy_deps.glew
```

### PyInstaller Options for Windows

- `--noconfirm`: Replace output directory without asking
- `--onefile`: Create single .exe file
- `--windowed`: Hide console window when running
- `--icon`: Set .exe icon
- `--name`: Set output .exe name
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.