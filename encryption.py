from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, kdf
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
#from base64 import urlsafe_b64encode, urlsafe_b64decode
import os

def derive_key(master_password, salt):
    # Key Derivation Function (KDF)
    kdf_instance = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32,  # 256-bit key for AES-256
        backend=default_backend()
    )

    key = kdf_instance.derive(master_password.encode('utf-8'))
    return key

def encrypt_file(master_password, input_file_path, output_file_path):
    # Generate a random salt
    salt = os.urandom(16)

    # Derive the key from the master password and salt
    key = derive_key(master_password, salt)

    # Read the plaintext from the input file
    with open(input_file_path, 'rb') as file:
        plaintext = file.read()

    # Generate a random IV (Initialization Vector)
    iv = os.urandom(16)

    # Encrypt the plaintext using AES in CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    # Write the salt, IV, and ciphertext to the output file
    with open(output_file_path, 'wb') as file:
        file.write(salt + iv + ciphertext)

def decrypt_file(master_password, input_file_path, output_file_path):
    # Read the salt, IV, and ciphertext from the input file
    with open(input_file_path, 'rb') as file:
        salt = file.read(16)
        iv = file.read(16)
        ciphertext = file.read()

    # Derive the key from the master password and salt
    key = derive_key(master_password, salt)

    # Decrypt the ciphertext using AES in CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Write the decrypted plaintext to the output file
    with open(output_file_path, 'wb') as file:
        file.write(plaintext)

# Example usage:
#master_password = "your_secure_master_password"
#input_file = "path/to/your/input/file.txt"
#output_file = "path/to/your/output/encrypted_file.enc"
#decrypt_file_to = "path/to/your/output/decrypted_file.txt"

# Encrypt file
#encrypt_file(master_password, input_file, output_file)

# Decrypt file
#decrypt_file(master_password, output_file, decrypt_file_to)
