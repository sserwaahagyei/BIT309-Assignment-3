# INFORMATION SYSTEM SECURITY
# ASSIGNMENT 3
# SECURE TEXT ENCODING AND DECODING
# Algorithm: AES-256-GCM

import os
import base64
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Save files in the same folder as this program
folder = Path(__file__).resolve().parent
KEY_FILE = folder / "secret_key.txt"
MESSAGE_FILE = folder / "encrypted_message.txt"


# Generate and save security key
def generate_key():
    key = AESGCM.generate_key(bit_length=256)
    encoded_key = base64.urlsafe_b64encode(key).decode()

    KEY_FILE.write_text(encoded_key, encoding="utf-8")

    print("\nSecurity key generated successfully!")
    print("Key saved in secret_key.txt")


# Load saved security key
def load_key():
    if not KEY_FILE.exists():
        raise FileNotFoundError("Generate a security key first.")

    key_text = KEY_FILE.read_text(encoding="utf-8").strip()
    key = base64.urlsafe_b64decode(key_text)

    if len(key) != 32:
        raise ValueError("Invalid security key.")

    return key


# Encrypt text
def encrypt_text():
    key = load_key()
    message = input("\nEnter your message: ")

    aes = AESGCM(key)
    nonce = os.urandom(12)

    encrypted = aes.encrypt(
        nonce, message.encode("utf-8"), None
    )

    result = base64.urlsafe_b64encode(
        nonce + encrypted
    ).decode()

    MESSAGE_FILE.write_text(result, encoding="utf-8")

    print("\nMessage encrypted successfully!")
    print("Encrypted message saved in encrypted_message.txt")


# Decrypt text
def decrypt_text():
    key = load_key()

    if not MESSAGE_FILE.exists():
        raise FileNotFoundError("No encrypted message found.")

    ciphertext = MESSAGE_FILE.read_text(
        encoding="utf-8"
    ).strip()

    data = base64.urlsafe_b64decode(ciphertext)

    nonce = data[:12]
    encrypted = data[12:]

    aes = AESGCM(key)
    decrypted = aes.decrypt(nonce, encrypted, None)

    print("\nDecrypted Message:")
    print(decrypted.decode("utf-8"))


# Main program
def main():
    while True:
        print("\n================================")
        print("   SECURE TEXT ENCRYPTION")
        print("        AES-256-GCM")
        print("================================")
        print("1. Generate Security Key")
        print("2. Encrypt Text")
        print("3. Decrypt Text")
        print("4. Exit")

        choice = input("\nChoose an option: ")

        try:
            if choice == "1":
                generate_key()

            elif choice == "2":
                encrypt_text()

            elif choice == "3":
                decrypt_text()

            elif choice == "4":
                print("Thank you for using the system!")
                break

            else:
                print("Invalid option. Try again.")

        except Exception as error:
            print("\nOperation failed:", error)


if __name__ == "__main__":
    main()