from werkzeug.security import generate_password_hash, check_password_hash

# Generate a new hash
password = "admin123"
hash = generate_password_hash(password, method='pbkdf2:sha256')
print(f"Generated hash: {hash}")

# Test the hash
is_valid = check_password_hash(hash, password)
print(f"Hash verification test: {'Success' if is_valid else 'Failed'}")

# Use this hash in your database_setup.sql 

# This is some sample text that i want to type to test out the smooth caret feature, it messes up when u try to se ctrl + backspace, its really weird and glitches when you try to do that thing. 