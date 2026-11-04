# Sistem Manajemen Perpustakaan

Aplikasi desktop Sistem Manajemen Perpustakaan berbasis Python dengan pola arsitektur MVC. Aplikasi memiliki fitur login dengan password ter-hash SHA-256, otorisasi berdasarkan role (admin dan anggota), serta pengelolaan data buku dan anggota yang tersimpan di database MySQL. Antarmukanya dibangun dengan CustomTkinter.

## Struktur Direktori

```
Modul3/
├── .github/workflows/ci_pipeline.yml   # Konfigurasi CI GitHub Actions
├── config/                             # Konfigurasi koneksi database
├── models/                             # Model: akses data (user, buku, anggota)
├── views/                              # View: tampilan antarmuka (login, buku, anggota)
├── controllers/                        # Controller: logika aplikasi (auth, buku, anggota)
├── tests/                              # Unit test (pytest)
├── main.py                             # Titik masuk aplikasi
├── pytest.ini                          # Konfigurasi pytest
└── requirements.txt                    # Daftar dependensi
```

## Instalasi dan Konfigurasi Database

1. Pastikan Python 3.11 atau lebih baru, Git, dan Laragon sudah terpasang.
2. Clone repositori dan masuk ke foldernya:

   ```
   git clone https://github.com/mohreskihidayat6-wq/Modul_3RPL.git
   cd Modul_3RPL
   ```

3. Buat virtual environment, aktifkan, lalu pasang dependensi:

   ```
   python -m venv env
   env\Scripts\activate
   pip install -r requirements.txt
   ```

4. Jalankan MySQL di Laragon, lalu buat database dan tabel (sesuaikan dengan skema yang dipakai):

   ```sql
   CREATE DATABASE db_perpustakaan;
   USE db_perpustakaan;

   CREATE TABLE users (
       id_user INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(50) NOT NULL UNIQUE,
       password VARCHAR(64) NOT NULL,
       role VARCHAR(20) NOT NULL
   );

   CREATE TABLE buku (
       id_buku INT AUTO_INCREMENT PRIMARY KEY,
       judul VARCHAR(150) NOT NULL,
       penulis VARCHAR(100) NOT NULL,
       tahun_terbit INT NOT NULL
   );
   ```

5. Sesuaikan host, user, password, dan nama database di `config/database.py`.
6. Daftarkan akun awal. Password otomatis di-hash SHA-256:

   ```python
   from models.user_model import UserModel
   UserModel().register_user("admin1", "admin123", "admin")
   ```

## Cara Menjalankan Aplikasi

Pastikan MySQL di Laragon menyala, lalu jalankan:

```
python main.py
```

Login dengan akun terdaftar. Role `admin` dapat menambah, memperbarui, dan menghapus data, sedangkan role `anggota` hanya dapat melihat data.

Untuk menjalankan unit test:

```
pytest -v
```

Untuk membuat berkas `.exe`:

```
pyinstaller --noconfirm --onefile --windowed --name "AplikasiPerpustakaan" main.py
```

Hasilnya ada di folder `dist/`.