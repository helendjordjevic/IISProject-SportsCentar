from passlib.context import CryptContext

# Postavljamo Argon2 kao shemu
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Lozinka za sve korisnike
plain_password = "123"

# Test korisnici
users = [
    ("Helena", "Djordjevic", "helendjordjevic@gmail.com", "ADMIN"),
    ("Sava", "Sredojevic", "sava@example.com", "INSTRUCTOR"),
    ("Maja", "Djordjevic", "maja@example.com", "CLIENT")
]

# Generišemo SQL INSERT naredbe
for first, last, email, user_type in users:
    hashed_pw = hash_password(plain_password)
    print(f"INSERT INTO users (first_name, last_name, email, hashed_password, user_type, sports_center_id) "
          f"VALUES ('{first}', '{last}', '{email}', '{hashed_pw}', '{user_type}', NULL);")
