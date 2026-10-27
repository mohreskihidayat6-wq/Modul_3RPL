import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.buku_model import BukuModel


import customtkinter as ctk
from tkinter import ttk

ctk.set_appearance_mode("light")


class BukuView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Manajemen Perpustakaan")
        self.geometry("800x450")

        # Konfigurasi Grid Utama (1 Baris, 2 Kolom)
        self.grid_columnconfigure(0, weight=1)  # Kolom Kiri (Form)
        self.grid_columnconfigure(1, weight=2)  # Kolom Kanan (Tabel lebih lebar)
        self.grid_rowconfigure(0, weight=1)

        # ----------------------------------------
        # FRAME KIRI: FORMULIR INPUT BUKU
        # ----------------------------------------
        self.frame_kiri = ctk.CTkFrame(self)
        self.frame_kiri.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(self.frame_kiri, text="Form Data Buku", font=("Arial", 16, "bold")).pack(pady=15)

        # Komponen Input
        self.entry_judul = ctk.CTkEntry(self.frame_kiri, placeholder_text="Masukkan Judul Buku")
        self.entry_judul.pack(pady=10, padx=15, fill="x")

        self.entry_penulis = ctk.CTkEntry(self.frame_kiri, placeholder_text="Masukkan Nama Penulis")
        self.entry_penulis.pack(pady=10, padx=15, fill="x")

        self.entry_tahun = ctk.CTkEntry(self.frame_kiri, placeholder_text="Tahun Terbit (Misal: 2024)")
        self.entry_tahun.pack(pady=10, padx=15, fill="x")

        # Tombol Aksi
        self.btn_simpan = ctk.CTkButton(self.frame_kiri, text="Simpan Data", fg_color="green")
        self.btn_simpan.pack(pady=10, padx=15, fill="x")

        # Tombol Perbarui Data (Update)
        self.btn_update = ctk.CTkButton(self.frame_kiri, text="Perbarui Data (Update)", fg_color="blue")
        self.btn_update.pack(pady=10, padx=15, fill="x")

        # Tombol Hapus Data (Delete)python views/buku_view.pypython views/buku_view.py
        self.btn_hapus = ctk.CTkButton(self.frame_kiri, text="Hapus Data (Delete)", fg_color="red")
        self.btn_hapus.pack(pady=10, padx=15, fill="x")

        # ----------------------------------------
        # FRAME KANAN: TABEL DAFTAR BUKU
        # ----------------------------------------
        self.frame_kanan = ctk.CTkFrame(self)
        self.frame_kanan.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        

        ctk.CTkLabel(self.frame_kanan, text="Daftar Koleksi Buku", font=("Arial", 16, "bold")).pack(pady=15)

        # Nama Pemilik
        ctk.CTkLabel(self.frame_kanan, text="Moh Reski Hidayat", font=("Arial", 12)).pack(pady=(0, 5))

        # Komponen Tabel (Treeview dari tkinter standar)
       

        # Komponen Tabel (Treeview dari tkinter standar)
        kolom = ("id", "judul", "penulis", "tahun")
        self.tabel = ttk.Treeview(self.frame_kanan, columns=kolom, show="headings", height=15)

        # Konfigurasi Header Tabel
        self.tabel.heading("id", text="ID")
        self.tabel.heading("judul", text="Judul Buku")
        self.tabel.heading("penulis", text="Penulis")
        self.tabel.heading("tahun", text="Tahun")

        # Konfigurasi Lebar Kolom
        self.tabel.column("id", width=40, anchor="center")
        self.tabel.column("judul", width=150)
        self.tabel.column("penulis", width=120)
        self.tabel.column("tahun", width=80, anchor="center")

        self.tabel.pack(fill="both", expand=True, padx=15, pady=10)
        self.model = BukuModel()
        self.id_terpilih = None
        self.btn_simpan.configure(command=self.simpan_data)
        self.btn_update.configure(command=self.update_data)
        self.btn_hapus.configure(command=self.hapus_data)
        self.tabel.bind("<<TreeviewSelect>>", self.pilih_data)
        self.tampilkan_data()
    def tampilkan_data(self):
        for item in self.tabel.get_children():
            self.tabel.delete(item)
        for b in self.model.get_all_buku():
            self.tabel.insert("", "end", values=(b["id_buku"], b["judul"], b["penulis"], b["tahun_terbit"]))

    def bersihkan_form(self):
        for e in (self.entry_judul, self.entry_penulis, self.entry_tahun):
            e.delete(0, "end")
        self.id_terpilih = None

    def simpan_data(self):
        judul = self.entry_judul.get().strip()
        penulis = self.entry_penulis.get().strip()
        tahun = self.entry_tahun.get().strip()
        if not (judul and penulis and tahun.isdigit()):
            print("Data tidak valid")
            return
        self.model.create_buku(judul, penulis, int(tahun))
        self.bersihkan_form()
        self.tampilkan_data()

    def pilih_data(self, event):
        pilih = self.tabel.selection()
        if not pilih:
            return
        id_buku, judul, penulis, tahun = self.tabel.item(pilih[0])["values"]
        self.id_terpilih = id_buku
        for e, v in ((self.entry_judul, judul), (self.entry_penulis, penulis), (self.entry_tahun, tahun)):
            e.delete(0, "end")
            e.insert(0, v)

    def update_data(self):
        if self.id_terpilih is None:
            return
        self.model.update_buku(self.id_terpilih, self.entry_judul.get(), self.entry_penulis.get(), int(self.entry_tahun.get()))
        self.bersihkan_form()
        self.tampilkan_data()

    def hapus_data(self):
        if self.id_terpilih is None:
            return
        self.model.delete_buku(self.id_terpilih)
        self.bersihkan_form()
        self.tampilkan_data()
# Blok eksekusi untuk menguji tampilan grafis
if __name__ == "__main__":
    app = BukuView()
    app.mainloop()