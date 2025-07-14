#!/bin/bash

if [ $EUID -ne 0 ]; then
	echo "$(basename $0) must be run as root"
	exit 1
fi

# get the directory of this script
work_dir="$(realpath $0|rev|cut -d '/' -f2-|rev)"

# configuration variables for the iso
output_dir="${work_dir}/output"
script_dir="${work_dir}/atomix"
temp_dir="${work_dir}/temp"

# create output directory if it doesn't exist yet
rm -rf "${output_dir}"
mkdir -p "${output_dir}"

rm -rf "${temp_dir}"
mkdir -p "${temp_dir}"

ADDITIONAL_PACKAGES="\
	https://github.com/Atomix-Linux/atomixinstall/releases/download/0.0.3-alpha/atomixinstall-0.0.2-1-any.pkg.tar.zst \
"

LOCAL_REPO="${script_dir}/extra_pkg"
mkdir -p ${LOCAL_REPO}
curl -L --remote-name-all --output-dir ${LOCAL_REPO} ${ADDITIONAL_PACKAGES}

repo-add ${LOCAL_REPO}/atomix.db.tar.gz ${LOCAL_REPO}/*.pkg.*
sed "s|LOCAL_REPO|$LOCAL_REPO|g" $script_dir/pacman.conf.template > $script_dir/pacman.conf

# make the container build the iso
mkarchiso -v -w "${temp_dir}" -o "${output_dir}" "${script_dir}"

# allow git command to work
git config --global --add safe.directory "${work_dir}"

ISO_FILE_PATH=`ls ${output_dir}/*.iso`
ISO_FILE_NAME=`basename "${ISO_FILE_PATH}"`
VERSION=`echo "${ISO_FILE_NAME}" | cut -c11-20 | sed 's/\./-/g'`
ID=`git rev-parse --short HEAD`

pushd ${output_dir}
sha256sum ${ISO_FILE_NAME} > sha256sum.txt
cat sha256sum.txt
popd

if [ -f "${GITHUB_OUTPUT}" ]; then
	echo "iso_file_name=${ISO_FILE_NAME}" >> "${GITHUB_OUTPUT}"
	echo "version=${VERSION}" >> "${GITHUB_OUTPUT}"
	echo "id=${ID}" >> "${GITHUB_OUTPUT}"
else
	echo "No github output file set"
fi
