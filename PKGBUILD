# Maintainer: Your Name <your.email@example.com>
pkgname=gitbutler-appimage
pkgver=0.16.7
pkgrel=1
pkgdesc="A Git client for simultaneous branches on top of your existing workflow"
arch=('x86_64')
url="https://gitbutler.com"
license=('custom')
depends=('fuse2' 'gtk3' 'webkit2gtk')
optdepends=('git: For Git operations')
install=${pkgname}.install
provides=('gitbutler')
conflicts=('gitbutler' 'gitbutler-bin')
source=("https://releases.gitbutler.com/releases/release/${pkgver}-2433/linux/x86_64/GitButler_${pkgver}_amd64.AppImage.tar.gz")
sha256sums=('SKIP')  # Replace with actual checksum

prepare() {
    cd "${srcdir}"
    tar -xzf "GitButler_${pkgver}_amd64.AppImage.tar.gz"
    chmod +x "GitButler_${pkgver}_amd64.AppImage"
}

build() {
    cd "${srcdir}"
    # Extract AppImage to get icons and desktop file
    ./GitButler_${pkgver}_amd64.AppImage --appimage-extract
}

package() {
    cd "${srcdir}"

    # Install the AppImage
    install -Dm755 "GitButler_${pkgver}_amd64.AppImage" "${pkgdir}/opt/GitButler/gitbutler.AppImage"

    # Create wrapper script with proper environment
    install -Dm755 /dev/stdin "${pkgdir}/usr/bin/gitbutler" << 'EOF'
#!/bin/bash
export GDK_BACKEND=x11
exec /opt/GitButler/gitbutler.AppImage "$@"
EOF

    # Install desktop file
    install -Dm644 squashfs-root/GitButler.desktop "${pkgdir}/usr/share/applications/GitButler.desktop"

    # Modify desktop file to use wrapper script
    sed -i 's|Exec=.*|Exec=gitbutler|g' "${pkgdir}/usr/share/applications/GitButler.desktop"

    # Install all available icons
    find squashfs-root/usr/share/icons/hicolor -name "gitbutler-tauri.png" | while read icon; do
        rel_path=${icon#squashfs-root/usr/share/icons/hicolor/}
        install -Dm644 "$icon" "${pkgdir}/usr/share/icons/hicolor/${rel_path}"
    done

    # Also check for icons in root directory of AppImage
    if [ -f "squashfs-root/gitbutler-tauri.png" ]; then
        install -Dm644 "squashfs-root/gitbutler-tauri.png" \
            "${pkgdir}/usr/share/icons/hicolor/256x256/apps/gitbutler-tauri.png"
    fi

    # Install license (if available in AppImage)
    if [ -f "squashfs-root/LICENSE" ]; then
        install -Dm644 "squashfs-root/LICENSE" "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
    fi
}