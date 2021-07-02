# Project: sql
# Author: absin
# Date: 2021-07-02
# DESC:

# Encryption and Decryption for user password
from cryptography.fernet import Fernet

cipher_key = Fernet.generate_key()


def encrypt(password):
    # encrypt will return bytes
    cipher_func = Fernet(cipher_key)
    # encrypt data should be bytes
    encrypted_password = cipher_func.encrypt(password.encode('utf-8'))
    # decode to string to save in db as varchar type
    return encrypted_password.decode('utf-8')


def decrypt(encrypted_password):
    cipher_func = Fernet(cipher_key)
    # encode string to byte to decrypt
    byte_encrypted_password = encrypted_password.encode('utf-8')
    # decrypt the password
    decrypted_password = cipher_func.decrypt(byte_encrypted_password)
    # decode to string to compare user input password
    return decrypted_password.decode('utf-8')
