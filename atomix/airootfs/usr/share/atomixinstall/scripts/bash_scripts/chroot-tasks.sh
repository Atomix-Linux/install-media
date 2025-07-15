#!/bin/bash

set -e


echo "Creating User..."
useradd -m -G wheel "${USERNAME}"
echo "${USERNAME}:${PASSWORD}" | chpasswd

echo "Setting language, timezone, keyboard layout and hostname..."
echo "${LANG}" > /etc/locale.gen
locale-gen
echo "LANG=${LOCALE_CODE}" > /etc/locale.conf
timedatectl set-timezone "${TIMEZONE}"
hostnamectl set-hostname "${HOSTNAME}"
localectl set-keymap "${KEYBOARD_LAYOUT}"

echo "Generating initcpio..."

echo '
ALL_config="/etc/mkinitcpio.conf"
ALL_kver="/boot/vmlinuz-linux"
ALL_microcode=(/boot/*-ucode.img)

PRESETS="default"

default_image="/boot/initramfs-linux.img"
' > /etc/mkinitcpio.d/\${NAME%%-*}.preset

mkinitcpio -p ${NAME%%-*}
