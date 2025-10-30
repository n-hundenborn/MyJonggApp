# Release Guide

This project uses GitHub Actions to automatically build executables for Windows and Linux.

## Creating a New Release

### Option 1: Using Git Tags (Recommended)

1. **Commit and push all changes:**
   ```bash
   git add .
   git commit -m "Prepare for release v1.0.0"
   git push
   ```

2. **Create and push a version tag:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

3. **Wait for GitHub Actions:**
   - Go to your repository on GitHub
   - Click the "Actions" tab
   - Watch the build progress (~10-15 minutes)

4. **Download your executables:**
   - Go to "Releases" tab
   - Your new release will appear with both Windows and Linux builds attached

### Option 2: Manual Trigger (For Testing)

1. Go to your repository on GitHub
2. Click "Actions" tab
3. Select "Build Cross-Platform Executables" workflow
4. Click "Run workflow" button
5. Select branch and click "Run workflow"
6. Executables will be available as artifacts (not as a release)

## Version Naming Convention

Use semantic versioning:
- `v1.0.0` - Major release
- `v1.1.0` - Minor update (new features)
- `v1.0.1` - Patch (bug fixes)

## What Happens Automatically

When you push a tag starting with `v`:

1. ✅ Windows executable is built (`MyJongg Calculator.exe`)
2. ✅ Linux executable is built (`MyJongg-Calculator`)
3. ✅ Both are packaged (zip for Windows, tar.gz for Linux)
4. ✅ GitHub Release is created with:
   - Release notes
   - Download links
   - Installation instructions
   - Both executables attached

## Troubleshooting

### Build fails on Windows
- Check that `requirements.lock` has all dependencies
- Verify `app.spec` is correct
- Check Actions logs for specific errors

### Build fails on Linux
- Check that `app_linux.spec` is correct
- Verify no Windows-specific code was added
- Check Actions logs for dependency issues

### Release not created
- Ensure you pushed a tag starting with `v` (e.g., `v1.0.0`)
- Check repository permissions in Settings > Actions

## Example Release Workflow

```bash
# 1. Make changes and test locally
python src/main.py

# 2. Commit changes
git add .
git commit -m "Add new feature X"
git push

# 3. Create release
git tag v1.2.0
git push origin v1.2.0

# 4. Wait ~10 minutes, then check GitHub Releases page
```

## Deleting a Release/Tag

If you need to redo a release:

```bash
# Delete local tag
git tag -d v1.0.0

# Delete remote tag
git push --delete origin v1.0.0

# Delete the release on GitHub (via web UI)
# Then create the tag again
```

