#!/bin/bash
#
# Copyright (C) 2026 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

set -e

# Trik manipulasi jalur agar output pas di vendor/PriCamera/proprietary/
DEVICE=PriCamera
VENDOR=..

# Set direktori utama
ANDROID_ROOT="/home/f1ell/X"
MY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Panggil file extract_utils.sh lokal
if [ -f "${MY_DIR}/tools-local/extract_utils.sh" ]; then
    . "${MY_DIR}/tools-local/extract_utils.sh"
else
    echo "Error: Berkas utilitas lokal tidak ditemukan!"
    exit 1
fi

# Ambil argumen folder dump
SRC="$1"
if [ -z "${SRC}" ]; then
    SRC="adb"
fi

# INI KUNCINYA: Matikan paksa fungsi cek odex bawaan LineageOS agar tidak memicu error "An input file is expected!"
import_oat_files() {
    return 0
}

# Mulai jalankan proses otomatisasi
setup_vendor "${DEVICE}" "${VENDOR}" "${ANDROID_ROOT}"
extract "${MY_DIR}/proprietary-files.txt" "${SRC}" "${SECTION}"

if [ -z "${SECTION}" ]; then
    write_makefiles
fi

echo "Sukses! Seluruh berkas biner PriCamera berhasil diekstrak dengan bersih."

