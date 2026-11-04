from unittest.mock import MagicMock
from models.buku_model import BukuModel


def test_create_buku_berhasil():
    model = BukuModel()

    # Mock koneksi database agar tidak mengotori data asli
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    hasil = model.create_buku("Buku Testing", "Penulis QA", 2026)

    assert hasil is True
    mock_cursor.execute.assert_called_once()
    model.conn.commit.assert_called_once()


def test_get_all_buku_berhasil():
    model = BukuModel()

    data_palsu = [
        {'id_buku': 1, 'judul': 'Buku A', 'penulis': 'Penulis A', 'tahun_terbit': 2020},
        {'id_buku': 2, 'judul': 'Buku B', 'penulis': 'Penulis B', 'tahun_terbit': 2021},
    ]
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = data_palsu
    model.conn.cursor.return_value = mock_cursor

    hasil = model.get_all_buku()

    assert hasil == data_palsu
    assert len(hasil) == 2
    mock_cursor.execute.assert_called_once()