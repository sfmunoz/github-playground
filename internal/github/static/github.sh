#!/bin/bash
PROJECT_NAME="$1"
TAG="$2"
set -x -e -o pipefail
mkdir -p dist/rootfs/usr/bin dist/rootfs/usr/lib/extension-release.d dist/rootfs/usr/lib64
cp "dist/${PROJECT_NAME}_linux_amd64_v1/${PROJECT_NAME}" "dist/rootfs/usr/bin/${PROJECT_NAME}"
cat <<__EOF >"dist/rootfs/usr/lib/extension-release.d/extension-release.${PROJECT_NAME}-flatcar"
ID=flatcar
SYSEXT_LEVEL=1.0
ARCHITECTURE=x86-64
__EOF
#cp /usr/bin/tmux /usr/bin/rclone dist/rootfs/usr/bin
#bash -c "cp -a /usr/lib/x86_64-linux-gnu/libutempter.so* dist/rootfs/usr/lib64"
mksquashfs dist/rootfs dist/rootfs.raw -noappend -comp zstd -all-root
find dist -type f | sort | gzip -9 >dist/dist.txt.gz
find /usr/ -type f | sort | gzip -9 >dist/usr.txt.gz
dpkg -l | gzip -9 >dist/dpkg.txt.gz
gh release upload "$TAG" dist/dist.txt.gz dist/usr.txt.gz dist/dpkg.txt.gz
