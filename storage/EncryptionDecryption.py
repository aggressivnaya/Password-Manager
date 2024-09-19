from aes import AES

aess = AES(b'\x00' * 16)

def decryption(password):
    return (aess.decrypt_block(password)).decode('utf-8')

def encryption(password):
    return aess.encrypt_block(password.encode('utf-8'))