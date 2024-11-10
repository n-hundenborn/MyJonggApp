# Project Name

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

1. Install PyInstaller in your virtual environment:
```cmd
pipenv install pyinstaller
```

2. For Windows GUI applications, use this command:
```cmd
pyinstaller --noconfirm --onefile --windowed --icon=assets/icon.ico --name "App Name" main.py
```

Or if you have a spec file:
```cmd
pyinstaller app.spec
```

The executable will be created in the `dist` folder.

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
project/
│
├── main.py
├── Pipfile
├── Pipfile.lock
├── assets/
│   └── icon.ico
├── build/
└── dist/
    └── App.exe
```
