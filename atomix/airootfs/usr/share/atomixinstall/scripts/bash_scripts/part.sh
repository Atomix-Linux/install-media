#!/bin/bash

set -e
set -o pipefail

EFI_PART=$2
SYS_PART=$1

echo $EFI_PART
echo $SYS_PART


echo "[INFO] Changing EFI Label..."
dosfslabel "$EFI_PART" EFI

echo "[INFO] Formating System partiton (just in case)..."
mkfs.btrfs -f -L zenkai_root "$SYS_PART"
