#!/bin/bash

set -e

MOUNT_PATH="/tmp/zenkai_root"

NAME=$(echo /tmp/zenkai_root/*.img.tar.xz | cut -f 1 -d '.')
SUBVOL="/tmp/zenkai_root/deploys/${NAME}"

echo "Installing Bootloader (systemd-boot)..."
bootctl --esp-path=/tmp/zenkai_root/boot/ install

get_boot_cfg() {
    local version=${1}
    local amd_ucode=${2}
	local intel_ucode=${3}

echo "title ${version}
linux /${version}/vmlinuz-linux
${amd_ucode}
${intel_ucode}
initrd /${version}/initramfs-linux.img
options root=LABEL=zenkai_root rw rootflags=subvol=deploys/${version} quiet loglevel=3 rd.systemd.show_status=auto rd.udev.log_priority=3"


}

BOOT_CFG="${MOUNT_PATH}/boot/loader/entries/zenkai.conf"
mkdir -p ${MOUNT_PATH}/boot/loader/entries

mkdir -p ${MOUNT_PATH}/boot/${NAME}
cp ${SUBVOL}/boot/vmlinuz-linux ${MOUNT_PATH}/boot/${NAME}
cp ${SUBVOL}/boot/initramfs-linux.img ${MOUNT_PATH}/boot/${NAME}

AMD_UCODE=""
if [ -e ${SUBVOL}/boot/amd-ucode.img ] ; then
    cp ${SUBVOL}/boot/amd-ucode.img ${MOUNT_PATH}/boot/${NAME}
    AMD_UCODE="initrd /${NAME}/amd-ucode.img"
fi

INTEL_UCODE=""
if [ -e ${SUBVOL}/boot/intel-ucode.img ] ; then
    cp ${SUBVOL}/boot/intel-ucode.img ${MOUNT_PATH}/boot/${NAME}
    INTEL_UCODE="initrd /${NAME}/intel-ucode.img"
fi


get_boot_cfg "${NAME}" "${AMD_UCODE}" "${INTEL_UCODE}" > ${BOOT_CFG}
echo "default zenkai.conf" > ${MOUNT_PATH}/boot/loader/loader.conf

echo "Done."
