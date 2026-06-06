#!/usr/bin/env python3
import os
import sys

# Konfigurasi Jalur
DUMP_DIR = os.path.expanduser("~/dump")
# Path absolut ke folder proprietary tujuanmu
PROPRIETARY_DIR = os.path.expanduser("~/X/vendor/advan/X1/PriCamera/proprietary")

# 1. Koleksi berkas
found_files = []
apk_path = ""
so_files = []

print(f"🔎 Memindai berkas PriCamera di dump... (Output akan ke {PROPRIETARY_DIR})")
for root, dirs, files in os.walk(DUMP_DIR):
    for file in files:
        if any(keyword in file.lower() for keyword in ["pricamera", "bst", "jni", "opencv", "tensorflow", "tflite", "jpeg", "miravision", "pq"]):
            full_path = os.path.join(root, file)
            rel_path = full_path.split("/dump/")[-1]
            
            if rel_path.startswith("system/system/"):
                rel_path = rel_path.replace("system/system/", "system/")
            
            if rel_path not in found_files:
                found_files.append(rel_path)
                if file.endswith(".apk"):
                    apk_path = rel_path
                elif file.endswith(".so") and "lib64" in rel_path:
                    so_files.append(file)

if not found_files:
    print("❌ Tidak ditemukan berkas kamera!")
    sys.exit(1)

# Pastikan folder proprietary ada
os.makedirs(PROPRIETARY_DIR, exist_ok=True)

# 2. Generate proprietary-files.txt
print("📝 Menyusun proprietary-files.txt...")
with open("proprietary-files.txt", "w") as f:
    f.write("# Auto-generated PriCamera Blobs List\n\n")
    for x in sorted(found_files):
        # Setiap file akan diarahkan ke folder 'proprietary/'
        target = f"proprietary/{x}"
        f.write(f"{x};{target}\n")

# 3. Generate Android.bp
print("📦 Menyusun Android.bp...")
with open("Android.bp", "w") as b:
    b.write("// Auto-generated Blueprint for PriCamera Module\n\n")
    b.write("android_app_import {\n")
    b.write('    name: "PriCamera",\n')
    b.write('    owner: "advan",\n')
    # Path apk sekarang merujuk ke dalam folder proprietary/
    b.write(f'    apk: "proprietary/{apk_path}",\n')
    b.write("    preprocessed: true,\n")
    b.write("    presigned: true,\n")
    b.write("    dex_preopt: { enabled: false },\n")
    b.write("    system_ext_specific: true,\n")
    b.write("}\n")

print("✔️ Berhasil!")
print(f"🚀 Sekarang jalankan ekstraksi, file akan mendarat di: {PROPRIETARY_DIR}")
