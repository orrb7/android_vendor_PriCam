#!/bin/bash
#
# Copyright (C) 2026 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

set -e

# Supaya pas meleleh ke folder /home/f1ell/X/vendor/PriCamera/proprietary
DEVICE=PriCamera
VENDOR=..

ANDROID_ROOT="/home/f1ell/X"
MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "${MY_DIR}/tools-local/extract_utils.sh" ]; then
    . "${MY_DIR}/tools-local/extract_utils.sh"
else
    echo "Error: Berkas utilitas lokal tidak ditemukan!"
    exit 1
fi

SRC="$1"
if [ -z "${SRC}" ]; then
    SRC="adb"
fi

# Jalankan inisialisasi vendor
setup_vendor "${DEVICE}" "${VENDOR}" "${ANDROID_ROOT}"

# Ambil fungsi dasar ekstrasi dengan tambahan parameter pembungkus kosong
# Tambahkan argumen penutup manual untuk mencegah pengecekan odex APK
extract "${MY_DIR}/proprietary-files.txt" "${SRC}" "${SECTION}"

if [ -z "${SECTION}" ]; then
    write_makefiles
fi

echo "Sukses! Seluruh berkas biner PriCamera berhasil diekstrak."
