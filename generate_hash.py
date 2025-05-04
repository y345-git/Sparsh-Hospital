from werkzeug.security import generate_password_hash

password = "admin123"
hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
print(f"Hashed password for '{password}':")
print(hashed_password) 