from models.buku_model import BukuModel

model = BukuModel()

# 1. Menguji fungsi Create (menambah buku baru)
print("Menambahkan data buku...")
model.create_buku("Pemrograman Python MVC", "Guido van Rossum", 2023)
print("Data berhasil disimpan ke Laragon MySQL!")

# 2. Menguji fungsi Read (menampilkan data)
print("\n=== Daftar Buku ===")
daftar_buku = model.get_all_buku()
for buku in daftar_buku:
    print(f"[{buku['id_buku']}] {buku['judul']} - {buku['penulis']} ({buku['tahun_terbit']})")

# 3. Menguji fungsi Update (mengubah data buku terakhir)
id_uji = daftar_buku[-1]['id_buku']
print("\nMengubah data buku...")
model.update_buku(id_uji, "Pemrograman Python MVC (Revisi)", "Guido van Rossum", 2024)
print("Data berhasil diubah!")

print("\n=== Daftar Buku Setelah Update ===")
for buku in model.get_all_buku():
    print(f"[{buku['id_buku']}] {buku['judul']} - {buku['penulis']} ({buku['tahun_terbit']})")

# 4. Menguji fungsi Delete (menghapus data buku yang diubah tadi)
print("\nMenghapus data buku...")
model.delete_buku(id_uji)
print("Data berhasil dihapus!")

print("\n=== Daftar Buku Setelah Delete ===")
for buku in model.get_all_buku():
    print(f"[{buku['id_buku']}] {buku['judul']} - {buku['penulis']} ({buku['tahun_terbit']})")