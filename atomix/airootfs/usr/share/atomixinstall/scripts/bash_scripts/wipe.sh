#!/bin/bash

set -e
set -o pipefail

DISK="Null"

DISK=$1
if [[ -z "$DISK" || ! -b "$DISK" ]]; then
  echo "USE: $0 /dev/sdX (np. /dev/sda lub /dev/nvme0n1"
  exit 1
fi


echo "[INFO] Creating GPT partition table..."
parted -s "$DISK" mklabel gpt

echo "[INFO] Creating EFI partition..."
parted -s "$DISK" mkpart ESP fat32 1MiB 513MiB
parted -s "$DISK" set 1 esp on

echo "[INFO] Creating system partition..."
parted -s "$DISK" mkpart primary btrfs 513MiB 100%

if [[ "$DISK" =~ nvme ]]; then
  EFI_PART="${DISK}p1"
  BTRFS_PART="${DISK}p2"
else
  EFI_PART="${DISK}1"
  BTRFS_PART="${DISK}2"
fi


echo "[INFO] Formating EFI as fat32..."
mkfs.fat -F32 -n EFI "$EFI_PART"

echo "[INFO] Formating System Partiton as btrfs..."
mkfs.btrfs -L zenkai_root "$BTRFS_PART"
