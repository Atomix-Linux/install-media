#!/bin/bash

set -e
set -o pipefail

MOUNT_PATH="/tmp/zenkai_root"

mkdir -p $MOUNT_PATH

mount -t btrfs -o nodatacow -L zenkai_root "$MOUNT_PATH"

btrfs subvolume create ${MOUNT_PATH}/var
btrfs subvolume create ${MOUNT_PATH}/home

mkdir ${MOUNT_PATH}/boot
mkdir ${MOUNT_PATH}/deploys
mkdir -p ${MOUNT_PATH}/etc
mkdir -p ${MOUNT_PATH}/.etc

mount -t vfat -L EFI "$MOUNT_PATH/boot"
