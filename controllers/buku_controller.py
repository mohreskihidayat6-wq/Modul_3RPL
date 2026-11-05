import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView


class BukuController:
    def __init__(self, user_role="anggota"):
        self.user_role = user_role
        self.model = BukuModel()
        self.view = BukuView()
        self.id_terpilih = None

        # Menampilkan informasi role pada judul jendela aplikasi
        self.view.title(f"Sistem Manajemen Perpustakaan - Mode: {self.user_role.upper()}")

        # Binding tombol dan tabel
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_update.configure(command=self.perbarui_data)
        self.view.btn_hapus.configure(command=self.hapus_data)
        self.view.btn_logout.configure(command=self.logout)
        self.view.tabel.bind("<<TreeviewSelect>>", self.pilih_baris)

        # OTORISASI: Jika bukan admin, nonaktifkan form input dan tombol aksi
        if self.user_role != "admin":
            self.view.btn_simpan.configure(state="disabled", text="Akses Terkunci (Khusus Admin)")
            self.view.btn_update.configure(state="disabled", text="Akses Terkunci (Khusus Admin)")
            self.view.btn_hapus.configure(state="disabled", text="Akses Terkunci (Khusus Admin)")
            self.view.entry_judul.configure(state="disabled")
            self.view.entry_penulis.configure(state="disabled")
            self.view.entry_tahun.configure(state="disabled")

        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)
        for buku in self.model.get_all_buku():
            self.view.tabel.insert(
                "", "end",
                values=(buku['id_buku'], buku['judul'], buku['penulis'], buku['tahun_terbit'])
            )

    def bersihkan_form(self):
        self.view.entry_judul.delete(0, 'end')
        self.view.entry_penulis.delete(0, 'end')
        self.view.entry_tahun.delete(0, 'end')
        self.id_terpilih = None

    def pilih_baris(self, event):
        # Anggota hanya melihat data, form tetap terkunci
        if self.user_role != "admin":
            return
        pilihan = self.view.tabel.selection()
        if not pilihan:
            return
        nilai = self.view.tabel.item(pilihan[0])['values']

        # Ambil id_buku dari baris yang diklik
        self.id_terpilih = nilai[0]

        self.view.entry_judul.delete(0, 'end')
        self.view.entry_penulis.delete(0, 'end')
        self.view.entry_tahun.delete(0, 'end')
        self.view.entry_judul.insert(0, str(nilai[1]))
        self.view.entry_penulis.insert(0, str(nilai[2]))
        self.view.entry_tahun.insert(0, str(nilai[3]))

    def _ambil_form(self):
        judul = self.view.entry_judul.get().strip()
        penulis = self.view.entry_penulis.get().strip()
        tahun = self.view.entry_tahun.get().strip()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return None
        if not tahun.isdigit():
            messagebox.showwarning("Peringatan", "Tahun terbit harus berupa angka!")
            return None
        return judul, penulis, int(tahun)

    def simpan_data(self):
        # Proteksi ganda di level Controller
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk menambah data!")
            return

        data = self._ambil_form()
        if data is None:
            return

        try:
            berhasil = self.model.create_buku(*data)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan data:\n{e}")
            return

        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal menyimpan data (koneksi database tidak tersedia).")

    def perbarui_data(self):
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk mengubah data!")
            return
        if self.id_terpilih is None:
            messagebox.showwarning("Peringatan", "Pilih data di tabel terlebih dahulu!")
            return

        data = self._ambil_form()
        if data is None:
            return

        if self.model.update_buku(self.id_terpilih, *data):
            messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", f"Gagal memperbarui data.\n{self.model.last_error}")

    def hapus_data(self):
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk menghapus data!")
            return
        if self.id_terpilih is None:
            messagebox.showwarning("Peringatan", "Pilih data di tabel terlebih dahulu!")
            return
        if not messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data ini?"):
            return

        if self.model.delete_buku(self.id_terpilih):
            messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", f"Gagal menghapus data.\n{self.model.last_error}")

    def logout(self):
        from controllers.auth_controller import AuthController  # di dalam method agar tidak circular import
        self.view.destroy()
        AuthController().run()

    def run(self):
        self.view.mainloop()