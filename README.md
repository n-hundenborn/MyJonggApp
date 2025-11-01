# MyJongg Calculator

Cross-platform Mahjongg score calculator built with Kivy.

## 📥 Download Pre-Built Executables

**Don't want to build from source?** Download ready-to-run executables from the [Releases page](../../releases).

- **Windows**: Download `.zip`, extract, run `MyJongg Calculator.exe`
- **Linux**: Download `.tar.gz`, extract, run `./MyJongg-Calculator`

## 📖 Table of Contents

- [Download Pre-Built Executables](#-download-pre-built-executables)
- [Automated Releases (GitHub Actions)](#-automated-releases-github-actions)
- [Windows Installation & Build](#windows-installation-guide)
- [Linux Installation & Build](#linux-installation-guide)
- [Key Differences Between Platforms](#key-differences-between-platforms)
- [Development Quick Reference](#development-quick-reference)

---

## 🚀 Automated Releases (GitHub Actions)

This project uses GitHub Actions to automatically build executables for both platforms.

### Creating a Release

```bash
# 1. Commit your changes
git add .
git commit -m "Ready for release"
git push

# 2. Create and push a version tag
git tag v1.0.0
git push origin v1.0.0

# 3. Wait ~10 minutes - GitHub Actions builds both executables
# 4. Download from the Releases page
```

See [.github/RELEASE_GUIDE.md](.github/RELEASE_GUIDE.md) for detailed instructions.

---

## Platform-Specific Build Instructions

For manual/local builds:

- [Windows Installation & Build](#windows-installation-guide)
- [Linux Installation & Build](#linux-installation-guide)

---

## Windows Installation Guide

### Prerequisites
- Windows 10 or 11
- Python 3.8 or higher ([Download from python.org](https://www.python.org/downloads/))
  - ✅ Make sure to check "Add Python to PATH" during installation

### Setup Development Environment

1. Open Command Prompt as Administrator and install pipenv:
```cmd
pip install pipenv
```

2. Clone or download the repository and navigate to the project folder:
```cmd
cd path\to\project
```

3. Create virtual environment and install dependencies:
```cmd
pipenv install
```

4. Activate the virtual environment:
```cmd
pipenv shell
```

### Building the Windows Executable

#### Prerequisites
Make sure you have PyInstaller installed:
```cmd
pip install pyinstaller
```

Also install Windows-specific Kivy dependencies:
```cmd
pip install kivy_deps.sdl2 kivy_deps.glew
```

#### Build Commands

**Option 1: Using the build script (recommended)**
```cmd
build_windows.bat
```

**Option 2: Manual build**
```cmd
pyinstaller app.spec
```

The executable will be created in the `dist` folder as `MyJongg Calculator.exe`.

### PyInstaller Options for Windows

- `--noconfirm`: Replace output directory without asking
- `--onefile`: Create single .exe file
- `--windowed`: Hide console window when running
- `--icon`: Set .exe icon
- `--name`: Set output .exe name

### Common Windows Issues

1. **"Python is not recognized as an internal or external command"**
   - Solution: Reinstall Python with "Add Python to PATH" checked
   - Or manually add Python to System Environment Variables

2. **Missing DLL errors**
   - Install Visual C++ Redistributable:
   - Download from [Microsoft's website](https://aka.ms/vs/17/release/vc_redist.x64.exe)

3. **Anti-virus flags the .exe**
   - Add exclusion for your development folder
   - Use `--key` option with PyInstaller to sign your executable

### Quick Commands Reference

```cmd
# Create new environment
pipenv install

# Activate environment
pipenv shell

# Install new package
pipenv install package_name

# Build exe
pyinstaller app.spec

# Clean build files
rmdir /s /q build
rmdir /s /q dist
del *.spec
```

### Project Structure
```
MyJonggApp/
├── src/
│   ├── main.py
│   ├── game.kv
│   ├── backend/
│   └── frontend/
├── assets/
│   ├── icon.ico
│   └── icon.png
├── app.spec (Windows)
├── app_linux.spec (Linux)
├── build_windows.bat
├── build_linux.sh
├── pyproject.toml
└── requirements.lock
```

---

## Linux Installation Guide

### Prerequisites
- Python 3.9 or higher
- System development packages

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install -y python3-dev python3-pip python3-venv \
    libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
    libgstreamer1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
    libmtdev-dev xclip xsel
```

#### Fedora/RHEL
```bash
sudo dnf install -y python3-devel redhat-rpm-config \
    SDL2-devel SDL2_image-devel SDL2_mixer-devel SDL2_ttf-devel \
    gstreamer1-devel gstreamer1-plugins-base-devel \
    mesa-libGL-devel
```

#### Arch Linux
```bash
sudo pacman -S python python-pip sdl2 sdl2_image sdl2_mixer sdl2_ttf \
    gstreamer gst-plugins-base gst-plugins-good mesa
```

### Setup Development Environment

1. Clone or download the repository:
```bash
cd /path/to/MyJongApp
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.lock
```

Or with uv (faster):
```bash
pip install uv
uv pip install -r requirements.lock
```

### Building the Linux Executable

#### Prerequisites
Install PyInstaller:
```bash
pip install pyinstaller
```

#### Build Commands

**Option 1: Using the build script (recommended)**
```bash
chmod +x build_linux.sh
./build_linux.sh
```

**Option 2: Manual build**
```bash
pyinstaller app_linux.spec
```

The executable will be created in the `dist` folder as `MyJongg-Calculator`.

### Running the Application

#### Development Mode
```bash
source venv/bin/activate
cd src
python main.py
```

#### Production (after build)
```bash
./dist/MyJongg-Calculator
```

### Common Linux Issues

1. **Missing SDL2 libraries**
   - Install system packages listed in prerequisites above
   - Check with: `ldconfig -p | grep SDL2`

2. **Permission denied when running executable**
   ```bash
   chmod +x dist/MyJongg-Calculator
   ```

3. **Wayland display issues**
   - Try forcing X11: `export GDK_BACKEND=x11`
   - Or run with: `GDK_BACKEND=x11 ./dist/MyJongg-Calculator`

4. **File dialog issues**
   - Install: `sudo apt install python3-tk zenity`

---

## Key Differences Between Platforms

| Feature | Windows | Linux |
|---------|---------|-------|
| Spec File | `app.spec` | `app_linux.spec` |
| Build Script | `build_windows.bat` | `build_linux.sh` |
| Output | `MyJongg Calculator.exe` | `MyJongg-Calculator` |
| Icon Format | `.ico` | `.png` |
| Kivy Dependencies | `kivy_deps.sdl2`, `kivy_deps.glew` | System SDL2 packages |
| File Size | ~80-120 MB | ~60-90 MB |

---

## Development Quick Reference

### Windows
```cmd
# Setup
pip install -r requirements.lock
pip install kivy_deps.sdl2 kivy_deps.glew pyinstaller

# Run development
cd src
python main.py

# Build
build_windows.bat
```

### Linux
```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.lock pyinstaller

# Run development
cd src
python main.py

# Build
chmod +x build_linux.sh
./build_linux.sh
```
