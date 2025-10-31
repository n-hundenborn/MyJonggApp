# Release Guide

This guide explains how to create a new release of MyJongg Calculator.

## Quick Release Process

```bash
# 1. Ensure all changes are committed and pushed
git add .
git commit -m "Your changes"
git push

# 2. Create and push a version tag
git tag v1.0.0
git push origin v1.0.0

# 3. Wait ~10-15 minutes
# GitHub Actions will automatically:
# - Build Windows executable (.zip)
# - Build Linux executable (.tar.gz)
# - Create a new release with both files attached
```

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **v1.0.0** - Major release (breaking changes)
- **v1.1.0** - Minor release (new features, backwards compatible)
- **v1.0.1** - Patch release (bug fixes)

## What Happens Automatically

When you push a tag starting with `v`:

1. **Windows Build** (~8 minutes)
   - Installs Python and dependencies
   - Builds with PyInstaller
   - Creates `MyJongg-Calculator-Windows.zip`

2. **Linux Build** (~8 minutes)
   - Installs system libraries (SDL2, etc.)
   - Builds with PyInstaller
   - Creates `MyJongg-Calculator-Linux.tar.gz`

3. **Release Creation**
   - Creates GitHub Release with your tag
   - Attaches both executables
   - Includes installation instructions

## Monitoring the Build

1. Go to: `https://github.com/<your-username>/<repo-name>/actions`
2. Click on the latest "Build and Release" workflow
3. Watch progress of Windows and Linux builds
4. Once complete, check the Releases page

## Troubleshooting

**Build fails:**
- Check the Actions tab for error logs
- Ensure `requirements.lock` is up to date
- Verify `.spec` files are correct

**Release not created:**
- Tag must start with `v` (e.g., `v1.0.0`, not `1.0.0`)
- Check repository permissions (Actions needs write access)

**Deleting a failed release:**
```bash
# Delete remote tag
git push --delete origin v1.0.0

# Delete local tag
git tag -d v1.0.0

# Then create it again with the same or different version
```

## Manual Build (for testing)

Before creating a release, test builds locally:

**Windows:**
```cmd
build_windows.bat
```

**Linux:**
```bash
./build_linux.sh
```
