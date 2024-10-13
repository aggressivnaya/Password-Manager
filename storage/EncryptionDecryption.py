from aes import encrypt, decrypt

key = b'master key'
enc = lambda key, ciphertext: encrypt(key, ciphertext, 10000)
dec = lambda key, ciphertext: decrypt(key, ciphertext, 10000)

def encryptText(text):
    return enc(key, text).decode('utf-8')

def decryptText(text):
    return dec(key, text).decode('utf-8')