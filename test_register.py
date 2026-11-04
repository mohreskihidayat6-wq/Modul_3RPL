from models.user_model import UserModel

um = UserModel()
print(um.register_user("admin1", "admin123", "admin"))
print(um.register_user("anggota1", "anggota123", "anggota"))