from models.anggota_model import AnggotaModel

model = AnggotaModel()

# 1. Menguji fungsi Create
print("Menambahkan data anggota...")
model.create_anggota("Reski", "Palu")
print("Data anggota berhasil disimpan!")

# 2. Menguji fungsi Read
print("\n=== Daftar Anggota ===")
for anggota in model.get_all_anggota():
    print(f"[{anggota['id_anggota']}] {anggota['nama']} - {anggota['alamat']}")

    