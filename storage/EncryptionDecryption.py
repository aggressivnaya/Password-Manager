import os
from aes import AES, encrypt, decrypt

key = os.urandom(16)
iv = os.urandom(16)
aess = AES(b'\x00' * 16)

def decryption(password):
    return (aess.decrypt_block(password)).decode('utf-8')

def encryption(password):
    return aess.encrypt_block(password.encode('utf-8'))