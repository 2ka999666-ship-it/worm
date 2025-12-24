# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

# ================== CONFIG ==================
VAULT_DIR = "vault"
PASSWORD = "i love kali"   # الباسورد الثابت
SALT_FILE = "salt.bin"
ITERATIONS = 100_000
# ============================================

def get_salt():
    if not os.path.exists(SALT_FILE):
        salt = os.urandom(16)
        with open(SALT_FILE, "wb") as f:
            f.write(salt)
        return salt
    with open(SALT_FILE, "rb") as f:
        return f.read()

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # Fernet يحتاج 32 بايت
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))

def encrypt_files(cipher):
    if not os.path.exists(VAULT_DIR):
        print("Vault folder not found.")
        return

    for root, dirs, files in os.walk(VAULT_DIR):
        for filename in files:
            if filename.endswith(".enc"):
                continue

            path = os.path.join(root, filename)

            try:
                with open(path, "rb") as f:
                    data = f.read()

                encrypted = cipher.encrypt(data)

                with open(path + ".enc", "wb") as f:
                    f.write(encrypted)

                os.remove(path)
                print("[+] Encrypted:", path)

            except Exception as e:
                print("[-] Failed:", path, e)

def decrypt_files(cipher):
    if not os.path.exists(VAULT_DIR):
        print("Vault folder not found.")
        return

    for root, dirs, files in os.walk(VAULT_DIR):
        for filename in files:
            if not filename.endswith(".enc"):
                continue

            path = os.path.join(root, filename)

            try:
                with open(path, "rb") as f:
                    data = f.read()

                decrypted = cipher.decrypt(data)

                original_path = path[:-4]

                with open(original_path, "wb") as f:
                    f.write(decrypted)

                os.remove(path)
                print("[+] Decrypted:", original_path)

            except Exception as e:
                print("[-] Failed:", path, e)

def main():
    print("=== Secure Vault (Educational Encryption) ===")
    print("Password is fixed: 'i love kali'")

    salt = get_salt()
    key = derive_key(PASSWORD, salt)
    cipher = Fernet(key)

    choice = input("Encrypt or Decrypt (e/d): ").lower().strip()

    if choice == "e":
        encrypt_files(cipher)
    elif choice == "d":
        decrypt_files(cipher)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
