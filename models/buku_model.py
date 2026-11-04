from config.database import Database

class BukuModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "buku"
        self.last_error = ""

    def get_all_buku(self):
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.table_name}"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        return []

    def create_buku(self, judul, penulis, tahun_terbit):
        if self.conn:
            cursor = self.conn.cursor()
            query = f"INSERT INTO {self.table_name} (judul, penulis, tahun_terbit) VALUES (%s, %s, %s)"
            val = (judul, penulis, tahun_terbit)
            cursor.execute(query, val)
            self.conn.commit()
            cursor.close()
            return True
        return False

    def update_buku(self, id_buku, judul, penulis, tahun_terbit):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                query = f"UPDATE {self.table_name} SET judul = %s, penulis = %s, tahun_terbit = %s WHERE id_buku = %s"
                val = (judul, penulis, tahun_terbit, id_buku)
                cursor.execute(query, val)
                self.conn.commit()
                cursor.close()
                return True
            except Exception as e:
                self.conn.rollback()
                self.last_error = str(e)
                return False
        return False

    def delete_buku(self, id_buku):
        if self.conn:
            cursor = None
            try:
                cursor = self.conn.cursor()
                # Matikan sementara pengecekan foreign key agar data induk bisa dihapus
                cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
                query = f"DELETE FROM {self.table_name} WHERE id_buku = %s"
                cursor.execute(query, (id_buku,))
                self.conn.commit()
                return True
            except Exception as e:
                self.conn.rollback()
                self.last_error = str(e)
                return False
            finally:
                if cursor is not None:
                    try:
                        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
                        cursor.close()
                    except Exception:
                        pass
        return False