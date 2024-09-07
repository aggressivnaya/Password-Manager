import aes, os

key = os.urandom(16)
iv = os.urandom(16)

def decryption(password) -> str:
    return aes.AES(key).decrypt_ctr(password, iv)

def encryption(password) -> str:
    return aes.AES(key).encrypt_ctr(password, iv)