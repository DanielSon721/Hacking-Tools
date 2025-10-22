import os
from cryptography.fernet import Fernet

files = []

for file in os.listdir():
    if file == "ransomware.py" or file == "secret_key.key" or file == "decrypt.py":
        continue
    if os.path.isfile(file):
        files.append(file)

with open("secret_key.key", "rb") as key:
    secret_key = key.read()

for file in files:
    with open(file, "rb") as target:
        contents = target.read()
    decrypted_contents = Fernet(secret_key).decrypt(contents)

    with open(file, "wb") as target:
        target.write(decrypted_contents)