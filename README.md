# GitButler AppImage AUR - Automated Package 🤖

![AUR Version](https://img.shields.io/aur/version/gitbutler-appimage)
![AUR Last Modified](https://img.shields.io/aur/last-modified/gitbutler-appimage)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/quantmind-br/gitbutler-aur-automation/auto-update.yml)

Automated AUR package for GitButler using AppImage with GitHub Actions automation.

## Installation

```bash
# Via AUR helper
yay -S gitbutler-appimage

# Or manually
git clone https://aur.archlinux.org/gitbutler-appimage.git
cd gitbutler-appimage
makepkg -si
```

## Package Details

- **Type**: AppImage-based package
- **Dependencies**: fuse2, gtk3, webkit2gtk
- **Configuration**: X11 backend enabled for compatibility
- **Installation**: `/opt/GitButler/gitbutler.AppImage`
- **Desktop Integration**: Full icon and menu integration

## Usage

After installation:
- **Menu**: Search for "GitButler"
- **Terminal**: `gitbutler`
- **Direct**: `/opt/GitButler/gitbutler.AppImage`

## Automation

This package is **automatically updated** via GitHub Actions:

- **🔄 Monitoring**: Checks for new GitButler releases every 6 hours
- **📦 Building**: Validates and tests package before deployment
- **🚀 Publishing**: Automatically pushes updates to AUR
- **📊 Logging**: Full execution logs available

### Automation Status

- **Frequency**: Every 6 hours
- **Last Run**: ![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/quantmind-br/gitbutler-aur-automation/auto-update.yml)
- **Logs**: [View Actions](https://github.com/quantmind-br/gitbutler-aur-automation/actions)

## Repository Structure

```
├── .github/workflows/
│   └── auto-update.yml      # Main automation workflow
├── check_updates.py         # Release monitoring script
├── notify.py               # Notification system
├── PKGBUILD                # AUR package definition
├── .SRCINFO                # AUR metadata
└── gitbutler-appimage.install  # Installation hooks
```

## How It Works

1. **Monitor**: GitHub Actions checks GitButler releases
2. **Detect**: Script identifies new versions
3. **Update**: PKGBUILD and .SRCINFO are updated
4. **Validate**: Package configuration is tested
5. **Deploy**: Changes are pushed to AUR
6. **Notify**: Success/failure notifications sent

## Links

- **AUR Package**: https://aur.archlinux.org/packages/gitbutler-appimage
- **Upstream**: https://github.com/gitbutlerapp/gitbutler
- **Official Site**: https://gitbutler.com
- **Automation Logs**: [GitHub Actions](https://github.com/quantmind-br/gitbutler-aur-automation/actions)

## Support

For issues:
- **Package Problems**: Comment on AUR package
- **Automation Issues**: Open issue in this repository
- **GitButler Bugs**: Report to upstream repository