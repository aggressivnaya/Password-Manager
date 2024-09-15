from aes import AES, encrypt, decrypt

aess = AES(b'\x00' * 16)
iv = b'\x01' * 16

def decryption(password):
    return (aess.decrypt_cbc(password, iv)).decode('utf-8')

def encryption(password):
    return aess.encrypt_cbc(password.encode('utf-8'), iv)