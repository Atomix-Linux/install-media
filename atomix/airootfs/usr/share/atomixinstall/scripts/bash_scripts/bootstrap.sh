#!/bin/bash

set -e

# Nie ma znaczenie

NAME=$(echo /tmp/zenkai_root/*.img.tar.xz.part.aa | cut -f 1 -d '.')

cat /tmp/zenkai_root/$NAME.img.tar.xz.part.* > /tmp/zenkai_root/$NAME.img.tar.xz

tar xfO /tmp/zenkai_root/$NAME.img.tar.xz | btrfs receive --quiet /tmp/zenkai_root/deploys

echo "Bootstraped system."
