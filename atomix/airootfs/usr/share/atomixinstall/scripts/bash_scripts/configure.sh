#!/bin/bash

set -e
set -o pipefail

export USERNAME=$1
export PASSWORD=$2
export TIMEZONE=$3
export LANGUAGE=$4
export HOSTNAME=$5
export KEYBOARD_LAYOUT=$6
export LOCALE_CODE=$7

export NAME=$(echo /tmp/zenkai_root/*.img.tar.xz | cut -f 1 -d '.')
SUBVOL="/tmp/zenkai_root/deploys/${NAME}"

if [ -d /tmp/zenkai_root ]; then
    if [ -d "${SUBVOL}" ]; then

        cd ${SUBVOL}

        mount -t proc /proc proc/
        mount -t sysfs /sys sys/
        mount --rbind /dev dev/

        btrfs property set -fts ${SUBVOL} ro false
        chroot ${SUBVOL} /bin/bash -c "/usr/share/atomixinstall/scripts/bash_scripts/chroot-tasks.sh"

        # Set back to R/O permissions
        btrfs property set -fts ${SUBVOL} ro true
        # unmount filesystems
        umount -l ${SUBVOL}/proc
        umount -l ${SUBVOL}/sys
        mount --make-rslave ${SUBVOL}/dev
        umount -l ${SUBVOL}/dev
    else
        echo "Not development found"
        exit 1
    fi
else
    echo "Not exists"
fi
