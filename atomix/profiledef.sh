#!/usr/bin/env bash
# shellcheck disable=SC2034

iso_name="atomix-linux"
iso_label="ATOMIX_$(date --date="@${SOURCE_DATE_EPOCH:-$(date +%s)}" +%Y%m)"
iso_publisher="Atomix Linux <https://atomix-linux.github.io>"
iso_application="Atomix Linux Installer"
iso_version="$(date --date="@${SOURCE_DATE_EPOCH:-$(date +%s)}" +%Y.%m.%d)"
install_dir="arch"
buildmodes=('iso')
bootmodes=('uefi-x64.systemd-boot.esp' 'uefi-x64.systemd-boot.eltorito')
arch="x86_64"
pacman_conf="pacman.conf"
airootfs_image_type="squashfs"
airootfs_image_tool_options=('-comp' 'xz' '-Xbcj' 'x86' '-b' '1M' '-Xdict-size' '1M')
bootstrap_tarball_compression=('zstd' '-c' '-T0' '--auto-threads=logical' '--long' '-19')
file_permissions=(
  ["/etc/shadow"]="0:0:400"
  ["/root"]="0:0:750"
  ["/root/install.sh"]="0:0:755"
  ["/root/.automated_script.sh"]="0:0:755"
  ["/root/.gnupg"]="0:0:700"
  ["/usr/local/bin/choose-mirror"]="0:0:755"
  ["/usr/local/bin/Installation_guide"]="0:0:755"
  ["/usr/local/bin/livecd-sound"]="0:0:755"
  ["/usr/bin/__aldm-deploy"]="0:0:755"
  ["/usr/bin/aldm-bootstrap"]="0:0:755"
  ["/usr/bin/aldm-deploy"]="0:0:755"
  ["/usr/bin/aldm-chroot"]="0:0:755"
  ["/usr/bin/aldm-release"]="0:0:755"
)
