import hashlib

password = "my_secret_password"
# Encode string to bytes
password_bytes = password.encode('utf-8')
print(password_bytes)
# Create hash object (e.g., SHA-256)
hash_object = hashlib.sha256(password_bytes)
print(hash_object)
# Get hexadecimal digest
hashed_password = hash_object.hexdigest()
print(hashed_password)