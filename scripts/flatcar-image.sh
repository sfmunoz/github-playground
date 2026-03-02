#!/bin/bash

set -e -o pipefail

function error_and_exit {
  echo "error: $1" >&2
  exit 1
}

DIST="dist"
ROOTFS="${DIST}/rootfs"
METADATA_JSON="${DIST}/metadata.json"

[ -f "$METADATA_JSON" ] || error_and_exit "'${METADATA_JSON}' doesn't exist"

eval "$(jq -r '. | "export PROJECT_NAME=\"\(.project_name)\"\nexport TAG=\"\(.tag)\""' <"$METADATA_JSON")"

[ "$PROJECT_NAME" = "" ] && error_and_exit "undefined 'PROJECT_NAME'"
[ "$TAG" = "" ] && error_and_exit "undefined 'TAG'"

echo "PROJECT_NAME ... '${PROJECT_NAME}'"
echo "TAG ............ '${TAG}'"

FLATCAR_EXT="${PROJECT_NAME}-flatcar"
FLATCAR_RAW="${DIST}/${FLATCAR_EXT}.raw"

set -x

rm -rf "${ROOTFS}"
mkdir -p "${ROOTFS}/usr/bin" "${ROOTFS}/usr/lib/extension-release.d" "${ROOTFS}/usr/lib64"
cp "${DIST}/${PROJECT_NAME}_linux_amd64_v1/${PROJECT_NAME}" "${ROOTFS}/usr/bin/${PROJECT_NAME}"
cat <<__EOF >"${ROOTFS}/usr/lib/extension-release.d/extension-release.${FLATCAR_EXT}"
ID=flatcar
SYSEXT_LEVEL=1.0
ARCHITECTURE=x86-64
__EOF
cp /usr/bin/tmux "${ROOTFS}/usr/bin/tmux"
cp -a /usr/lib/x86_64-linux-gnu/libutempter.so* "${ROOTFS}/usr/lib64"
mksquashfs "${ROOTFS}" "${FLATCAR_RAW}" -noappend -comp zstd -all-root
[ "$GITHUB_TOKEN" = "" ] && exit 0 # don't upload in local environment
gh release upload "${TAG}" "${FLATCAR_RAW}"

# find dist -type f | sort | gzip -9 >"${DIST}/dist.txt.gz"
# find /usr/ -type f | sort | gzip -9 >"${DIST}/usr.txt.gz"
# dpkg -l | gzip -9 >"${DIST}/dpkg.txt.gz"
# gh release upload "${TAG}" "${DIST}/dist.txt.gz" "${DIST}/usr.txt.gz" "${DIST}/dpkg.txt.gz"
