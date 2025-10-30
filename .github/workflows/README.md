# GitHub Actions Workflows

## build-releases.yml

Automatically builds Windows and Linux executables for the MyJongg Calculator.

### Triggers

1. **Tag Push**: When you push a tag starting with `v` (e.g., `v1.0.0`)
   - Builds both executables
   - Creates a GitHub Release
   - Attaches executables to the release

2. **Manual**: Via GitHub UI Actions tab
   - Builds both executables
   - Uploads as artifacts (no release created)

### What It Does

#### Build Stage
- Runs on both `windows-latest` and `ubuntu-latest`
- Installs platform-specific dependencies
- Executes the appropriate build script
- Uploads executables as artifacts

#### Release Stage (tag push only)
- Downloads both executables
- Packages them (zip for Windows, tar.gz for Linux)
- Creates a GitHub Release with:
  - Automatic release notes
  - Download links
  - Installation instructions
  - Both packaged executables

### Build Time
- Windows: ~8-12 minutes
- Linux: ~5-8 minutes
- **Total**: ~10-15 minutes

### Free Tier Usage
- **Public repos**: Unlimited (free forever)
- **Private repos**: 2,000 minutes/month
- Each release uses ~20 minutes (both platforms)
- You can do ~100 releases per month on private repos

### Artifacts Retention
- Build artifacts are kept for 90 days
- Released executables are kept forever

### Permissions Required
- `contents: write` - For creating releases (already configured)

### Troubleshooting

**Build fails?**
- Check the Actions tab for detailed logs
- Verify all dependencies are in `requirements.lock`
- Ensure spec files are correct

**No release created?**
- Make sure you pushed a tag starting with `v`
- Check repository permissions: Settings > Actions > General

**Want to test without creating a release?**
- Use "workflow_dispatch" (manual trigger) from Actions tab
- Executables will be available as artifacts, not releases

