#!/usr/bin/env python3
import os
import sys

# Konfigurasi Jalur
DUMP_DIR = os.path.expanduser("~/dump")
VENDOR_PATH = "system_ext" # Karena sebagian besar blob PriCamera ada di system_ext

# 1. Koleksi berkas dari dump secara otomatis
found_files = []
apk_path = ""
so_files = []

print("🔎 Memindai berkas PriCamera di dump...")
for root, dirs, files in os.walk(DUMP_DIR):
    for file in files:
        # Cari berkas yang berkaitan dengan PriCamera / BST / PQ / Tensorflow
        if any(keyword in file.lower() for keyword in ["pricamera", "bst", "jni", "opencv", "tensorflow", "tflite", "jpeg", "miravision", "pq"]):
            full_path = os.path.join(root, file)
            # Ambil jalur setelah folder dump/partisi
            rel_path = full_path.split("/dump/")[-1]
            
            # Rapikan jalur jika ada double partisi (misal system/system/)
            if rel_path.startswith("system/system/"):
                rel_path = rel_path.replace("system/system/", "system/")
            elif rel_path.startswith("system_ext/"):
                pass
            
            if rel_path not in found_files:
                found_files.append(rel_path)
                if file.endswith(".apk"):
                    apk_path = rel_path
                elif file.endswith(".so") and "lib64" in rel_path:
                    so_files.append(file)

if not found_files:
    print("❌ Tidak ditemukan berkas kamera di ~/dump. Pastikan jalur dump benar!")
    sys.exit(1)

# 2. Generate proprietary-files.txt secara otomatis
print("📝 Menyusun proprietary-files.txt...")
with open("proprietary-files.txt", "w") as f:
    f.write("# Auto-generated PriCamera Blobs List\n\n")
    
    # Kelompokkan APK
    f.write("# Core Application\n")
    for x in sorted(found_files):
        if x.endswith(".apk"):
            f.write(f"{x};system_ext\n")
            
    # Kelompokkan Libraries dengan SYMLINK otomatis ke folder App
    f.write("\n# Shared Libraries & Symlinks\n")
    for x in sorted(found_files):
        if x.endswith(".so") and "lib64" in x:
            lib_name = os.path.basename(x)
            # Berikan aturan SYMLINK khusus library JNI internal agar terbaca aplikasi
            if any(k in lib_name for k in ["libBST", "libjni", "libopencv"]):
                f.write(f"{x};system_ext;SYMLINK=system_ext/app/PriCamera/lib/arm64/{lib_name}\n")
            else:
                f.write(f"{x};system_ext\n")

    # Kelompokkan Config (.cfg / non-binary)
    f.write("\n# Configuration Files\n")
    for x in sorted(found_files):
        if not x.endswith(".so") and not x.endswith(".apk") and not x.endswith(".odex") and not x.endswith(".vdex"):
            f.write(f"{x};system_ext\n")

print("✔️ proprietary-files.txt berhasil diperbarui!")

# 3. Generate Android.bp secara otomatis (Sinkron dengan lib64)
print("📦 Menyusun Android.bp...")
with open("Android.bp", "w") as b:
    b.write("// Auto-generated Blueprint for PriCamera Module\n\n")
    b.write("android_app_import {\n")
    b.write('    name: "PriCamera",\n')
    b.write('    owner: "advan",\n')
    b.write(f'    apk: "proprietary/{apk_path}",\n')
    b.write("    preprocessed: true,\n")
    b.write("    presigned: true,\n")
    b.write("    dex_preopt: {\n")
    b.write("        enabled: false,\n")
    b.write("    },\n")
    b.write("    system_ext_specific: true,\n")
    b.write("    symlinks: [\n")
    
    # Hanya daftarkan library utama ke symlink blueprint sebagai back-up linker
    for so in sorted(so_files):
        if any(k in so for k in ["libBST", "libjni", "libopencv"]):
            b.write(f'        "../../../lib64/{so}",\n')
            
    b.write("    ],\n")
    b.write("}\n")

print("✔️ Android.bp berhasil disinkronisasikan!")
print("🚀 Selesai! Jalankan ./extract-files.sh ~/dump sekarang.")
