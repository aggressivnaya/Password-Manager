from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# Key and initialization vector must be 16, 24, or 32 bytes long for AES
key = get_random_bytes(16)  # AES key (128-bit key)
iv = get_random_bytes(16)  # Initialization Vector for CBC mode

def aes_encrypt(plaintext, key, iv):
    # Convert plaintext to bytes if it's a string
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')
    
    # Pad the plaintext to be a multiple of the AES block size (16 bytes)
    padded_plaintext = pad(plaintext, AES.block_size)

    # Create a new AES cipher object in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Encrypt the padded plaintext
    ciphertext = cipher.encrypt(padded_plaintext)
    return ciphertext

def aes_decrypt(ciphertext, key, iv):
    # Create a new AES cipher object in CBC mode for decryption
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the ciphertext
    decrypted_padded_plaintext = cipher.decrypt(ciphertext)

    # Unpad the decrypted plaintext to get the original plaintext
    decrypted_plaintext = unpad(decrypted_padded_plaintext, AES.block_size)
    return decrypted_plaintext.decode('utf-8')

# Example usage
#plaintext = "This is a secret message"
#ciphertext = aes_encrypt(plaintext, key, iv)
#print(f"Encrypted: {ciphertext}")

#decrypted = aes_decrypt(ciphertext, key, iv)
#print(f"Decrypted: {decrypted}")
